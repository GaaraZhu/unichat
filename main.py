# -​*- coding: utf-8 -*​-
import sys
import logging
from unichat.bot import Bot

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s [%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    token = sys.argv[1]
    channel = sys.argv[2]
    googleApikey = sys.argv[3]
    bot = Bot(token, channel, googleApikey)
    print("Starting bot...")
    bot.bot_main()


if __name__ == "__main__":
    main()
