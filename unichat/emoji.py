# -​*- coding: utf-8 -*​-


class EmojiHandler():
    def __init__(self):
        self.w2s = dict()
        self.s2w = dict()
        with open("resources/emojis.txt") as emojiSource:
            for line in emojiSource:
                wechatEmoji, slackEmoji = line.replace('\n',
                                                       '').partition("=")[::2]
                self.w2s[wechatEmoji] = slackEmoji
                self.s2w[slackEmoji] = wechatEmoji

    def slack2WeChat(self, source, callback):
        return self._processEmoji(source, self.s2w, callback)

    def weChat2Slack(self, source, callback):
        return self._processEmoji(source, self.w2s, callback)

    def _processEmoji(self, source, emojiMappings, callback):
        emojis = list()
        for (key, value) in emojiMappings.items():
            if key in source:
                source = source.replace(key, "@@" + str(len(emojis)) + "@@")
                emojis.append(value)

        print("before translation: " + source)
        source = callback(source)
        print("after translation: " + source)

        for emoji in emojis:
            index = emojis.index(emoji)
            #ugly space caused by google translate api lol
            source = source.replace("@@ " + str(index) + " @@", emoji)

        return source
