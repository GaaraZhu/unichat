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
        self.related_channels = {}

    def attach_channel(self, name):
        c = self.client.server.channels.find(name)
        if c:
            logging.info("Listening on channel: %s" % c)
            self.related_channels[name] = c
        else:
            logging.info("Channel %s not found" % name)

    def __is_interesting_message(self, event):
        if u'type' not in event:
            return False
        if event[u'type'] != 'message':
            return False
        if event[u'user'] == self.my_id:
            return False
        for c in self.related_channels.values():
            if c.id == event[u'channel']:
                return True
        return False

    def read_messages_in_channels(self):
        events = self.client.rtm_read()
        return itertools.ifilter(self.__is_interesting_message, events)

    def send_message_to_channel(self, channel, message):
        pass

    def echo(self):
        for e in self.read_messages_in_channels():
            channel = e[u'channel']
            message = u'Reply: %s' % e[u'text']
            print "Replying message: %s" % message
            self.client.rtm_send_message(channel, message)
