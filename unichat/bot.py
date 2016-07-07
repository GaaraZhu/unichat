# -​*- coding: utf-8 -*​-
import logging
import time
import sys
import os
from contextlib import contextmanager

from itchat.client import client as WeChatClient
from emoji import EmojiHandler
from translator import Translator
from slack import UniChatSlackClient

@contextmanager
def tmp_file():
    tmp_filename = os.tmpnam()
    yield tmp_filename
    os.unlink(tmp_filename)


class Bot(object):
    def __init__(self, token, channelName, googleApikey):
        self.channelName = channelName
        self.slackClient = UniChatSlackClient(token)
        self.wechatGroup = None
        self.wechatClient = WeChatClient()
        self.translator = Translator(googleApikey)
        self.emojiHandler = EmojiHandler()
        self.media_types = set(['Picture', 'Recording', 'Video'])
        self.enableTranslator = False

    def bot_main(self):
        self.channel = self.slackClient.join_channel(self.channelName)
        self.wechatClient.auto_login()

        while True:
            try:
                group_messages = self.receive_wechat_group_msgs()
                self.process_wechat_messages(group_messages)
                slack_messages = self.slackClient.read_messages_in_channels()
                self.process_slack_messages(slack_messages)
                time.sleep(.5)
            except KeyboardInterrupt:
                logging.info("Stopping bot...")
                break
            except:
                logging.exception("Unexpected error")

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

    def forward_wechat_file(self, msg):
        with tmp_file() as file_name:
            download_func = msg['Text']
            logging.info("Saving WeChat file to " + file_name)
            download_func(file_name)
            #os.fsync() # Make sure the image is written to disk
            title = msg['ActualNickName'] + " shared a file"
            logging.info("Uploading image to slack: %s" % file_name)
            self.slackClient.send_file_to_channel(self.channel.id, file_name, title)

    def forward_slack_image(self, user_name, msg):
        with tmp_file() as file_name:
            logging.info("Saving Slack image to " + file_name)
            if self.slackClient.extract_file(msg, file_name):
                logging.info("Uploading image to WeChat: %s" % file_name)
                self.wechatClient.send_msg("%s shared a file: %s" % (user_name, msg[u'file'][u'name']), self.wechatGroup)
                self.wechatClient.send_image(file_name, self.wechatGroup)

    def process_wechat_messages(self, msgs):
        for msg in msgs:
            logging.info("WeChat group: %s" % msg['FromUserName'])
            if not self.wechatGroup:
                self.wechatGroup = msg['FromUserName']

            logging.debug("Got WeChat message: %s" % msg)
            logging.info("Sending message to slack: %s" % msg['Text'])
            if msg['Type'] in self.media_types:
                self.forward_wechat_file(msg)
            else:
                original_msg = msg['Text']
                nick_name = msg['ActualNickName']
                update_emoji_result = self.emojiHandler.weChat2Slack(original_msg, lambda x: x)
                if self.enableTranslator:
                    translate_result = self.emojiHandler.weChat2Slack(original_msg, self.translator.toEnglish)
                    message = u"%s: %s\n\n[Translation] %s" % (nick_name, update_emoji_result, translate_result)
                else:
                     message = u"%s: %s" % (nick_name, update_emoji_result)
                self.channel.send_message(message)# TODO Doesn't look so nice to use `channel` directly.

    def process_slack_messages(self, msgs):
        for msg in msgs:
            if self.wechatGroup:
                logging.debug("Got slack message: %s" % msg)
                logging.info("Sending message to wechat: %s" % msg[u'text'])
                user_name = self.slackClient.get_user_name(msg[u'user'])
                original_msg = msg[u'text']
                
                if u'subtype' in msg and msg[u'subtype'] == u'file_share':
                    self.forward_slack_image(user_name, msg)
                elif u'trans_on' == original_msg:
                    self.enableTranslator = True
                    self.channel.send_message(u"_Translation turned on_")
                elif u'trans_off' == original_msg:
                    self.enableTranslator = False
                    self.channel.send_message(u"_Translation turned off_")
                else:
                    update_emoji_result = self.emojiHandler.slack2WeChat(original_msg, lambda x: x)
                    if self.enableTranslator:
                        translate_result = self.emojiHandler.slack2WeChat(original_msg, self.translator.toChinese)
                        message = u"%s: %s\n\n[翻译] %s" % (user_name, update_emoji_result, translate_result)
                    else:
                        message = "%s: %s" % (user_name, update_emoji_result)

                    self.wechatClient.send_msg(message, self.wechatGroup)
                        
            else:
                logging.info("No WeChat group")