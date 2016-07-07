# Unichat

A bot that connects different IM services.

## Install

It's recommended to use virtualenv.

```
cd <project_dir>
virtualenv --no-site-packages venv
source venv/bin/activate
```

To install the dependencies:

```
git submodule init
git submodule update
pip install -r requirements.txt
pip install ItChat/
pip install python-slackclient/
```

## Run

To run the bot

```
python bot.py <slack_token> <slack_channel> <gapi_token>
```

A QR code image should pop up. Scan the QR code with mobile WeChat to start the
bot (log in with the bot account first).
