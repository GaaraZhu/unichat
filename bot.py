import logging
import time
import sys

from slack import UniChatSlackClient
from itchat.client import client as WeChatClient


class Bot(object):
    def __init__(self, token, channelName):
        self.channelName = channelName
        self.wechatClient = WeChatClient()
        self.slackClient = UniChatSlackClient(token)
        self.wechatGroup = None

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
            self.channel.send_message(msg['ActualNickName'] + ": " + msg['Content'])

    def process_slack_messages(self, msgs):
        for msg in msgs:
            if self.wechatGroup:
                print("Sending message to wechat: %s" % msg[u'text'])
                self.wechatClient.send_msg(msg[u'text'], self.wechatGroup)
            else:
                print("No WeChat group")


def main():
    token = sys.argv[1]
    channel = sys.argv[2]
    bot = Bot(token, channel)
    print("Starting bot...")
    bot.bot_main()


if __name__ == "__main__":
    main()
