# -​*- coding: utf-8 -*​-
from __future__ import print_function

from googleapiclient.discovery import build

class Translator:
    def __init__(self, key):
        self.service = build('translate', 'v2', developerKey = key)

    def toEnglish(self, message):
        return self.service.translations().list(
            target='en',
            q=[message]).execute().get(u'translations').pop().get(u'translatedText')

    def toChinese(self, message):
        return self.service.translations().list(
            target='zh-CN',
            q=[message]).execute().get(u'translations').pop().get(u'translatedText')