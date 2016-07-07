class EmojiHandler():
    def __init__(self):
        self.w2s = dict()
        self.s2w = dict()
        with open("resources/emojis.txt") as emojiSource:
            for line in emojiSource:
                wechatEmoji, slackEmoji = line.replace('\n','').partition("=")[::2]
                print("key: %s . value: %s"%(wechatEmoji, slackEmoji))
                self.w2s[wechatEmoji] = slackEmoji
                self.s2w[slackEmoji] = wechatEmoji

    def wechat2Slack(self, source):
        for (key, value) in self.w2s.items():
            source = source.replace(key, value)
        return source

    def slack2WeChat(self, source):
        print(self.s2w)
        for (key, value) in self.s2w.items():
            print("slack message: before: %s"%source)
            source = source.replace(key, value)
            print("slack message: after: %s"%source)
        return source