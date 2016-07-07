import logging
import itertools

from slackclient import SlackClient


class SlackException(Exception):
    def __init__(self, msg):
        self.msg = msg


class UniChatSlackClient(object):
    def __init__(self, token):
        sc = SlackClient(token)
        logging.info("Connecting to slack...")
        if not sc.rtm_connect():
            raise SlackException("Unable to connect to Slack (invalid token?)")
        logging.info("Connected to slack WebSocket")
        self.client = sc
        self.my_id = sc.server.login_data[u'self'][u'id']
        users = sc.server.login_data[u'users']
        self.team_members = dict([(user[u'id'], self.__name_tag(user)) for user in users])
        self.related_channels = {}

    def __name_tag(self, user):
        profile = user[u'profile']
        if u'first_name' in profile and u'last_name' in profile:
            return profile[u'first_name'] + " " + profile[u'last_name']
        else:
            return user[u'name']

    def attach_channel(self, name):
        c = self.client.server.channels.find(name)
        if c:
            logging.info("Listening on channel: %s" % c)
            self.related_channels[name] = c
            return c
        else:
            logging.info("Channel %s not found" % name)
            return None

    def __is_interesting_message(self, event):
        if u'type' not in event or u'user' not in event:
            return False
        if event[u'type'] != 'message':
            return False
        if event[u'user'] == self.my_id:
            return False
        for c in self.related_channels.values():
            if c.id == event[u'channel']:
                return True
        return False

    def get_user_name(self, user_id):
        return self.team_members.get(user_id, "unknown")

    def read_messages_in_channels(self):
        events = self.client.rtm_read()
        return [e for e in events if self.__is_interesting_message(e)]

    def send_message_to_channel(self, channel, message):
        self.client.rtm_send_message(channel, message)
