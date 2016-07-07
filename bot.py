import logging
import time
import sys

from GoogleApi import Translator
from slack import UniChatSlackClient
from itchat.client import client as WeChatClient


class Bot(object):
    def __init__(self, token, channelName, googleApikey):
        self.channelName = channelName
        self.slackClient = UniChatSlackClient(token)
        self.wechatGroup = None
        self.wechatClient = WeChatClient()
        self.translator = Translator(googleApikey)

    def bot_main(self):
        self.channel = self.slackClient.attach_channel(self.channelName)
        print("Channel: %s" % self.channel)

        self.wechatClient.auto_login()

        while True:
            group_messages = self.receive_wechat_group_msgs()
            self.process_wechat_messages(group_messages)
            slack_messages = self.slackClient.read_messages_in_channels()
            self.process_slack_messages(slack_messages)
            time.sleep(.5)

    def receive_wechat_group_msgs(self):
        client = self.wechatClient
        if not client.storageClass.msgList:
            return []
        msgs = []
        while client.storageClass.msgList:
            msg = client.storageClass.msgList.pop()
            if '@@' in msg.get('FromUserName'):
                msgs.append(msg)
        return msgs

    def process_wechat_messages(self, msgs):
        for msg in msgs:
            print("WeChat group: %s" % msg['FromUserName'])
            if not self.wechatGroup:
                self.wechatGroup = msg['FromUserName']
            print("Sending message to slack: %s" % msg['Content'])
            # TODO Doesn't look so nice to use `channel` directly.
            self.channel.send_message(msg['ActualNickName'] + ": " + msg['Content'])
            translatedMsg = self.translator.toEnglish(msg['Content'])
            self.channel.send_message("[Translation]: %s : %s" % (msg['ActualNickName'], translatedMsg))

    def process_slack_messages(self, msgs):
        for msg in msgs:
            if self.wechatGroup:
                print("Sending message to wechat: %s" % msg[u'text'])
                user_name = self.slackClient.get_user_name(msg[u'user'])

                translatedMsg = self.translator.toChinese(msg[u'text'])
                self.wechatClient.send_msg("[Translation]: %s : %s" % (user_name, translatedMsg), self.wechatGroup)
                self.wechatClient.send_msg(user_name + ": " + msg[u'text'], self.wechatGroup)
            else:
                print("No WeChat group")

def main():
    token = sys.argv[1]
    channel = sys.argv[2]
    googleApikey = sys.argv[3]
    bot = Bot(token, channel, googleApikey)
    print("Starting bot...")
    bot.bot_main()


if __name__ == "__main__":
    main()
