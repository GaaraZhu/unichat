# Unichat

## Background
As one of the world's most popular team collaboration tools, Slack is quite hot these years. When solving problems with our Chinese customers, they prefer to use WeChat as the communication tool. The drawbacks of using WeChat in that context are:

* Conversation history is not archived
* We can only invite people with a WeChat account to the conversation
* We need to switch between WeChat and Slack to sync some information to colleagues or to JIRA

So, we’ve come up with this idea of Unichat – a tool to make Slack the uniform messaging platform, no matter which application our customer is using (Slack, WeChat or even Line). This will mean that in the future, we can use Slack as both internal and external messaging service.

These functions have been included in the first release:
* Send text message from WeChat to Slack and vice versa
* Enable translation for text messages from Chinese to English and vice versa
* Send attachment (image/pdf/excel/video etc) from WeChat to Slack and vice versa
* Auto translation for emojis

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

To run unichat

```
python main.py <slack_token> <slack_channel> <gapi_token>
```

A QR code image should pop up. Scan the QR code with mobile WeChat to start the
journey (send messages from WeChat/Line first to start the conversaction).
