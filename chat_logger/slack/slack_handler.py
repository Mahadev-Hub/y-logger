import os
from slack_sdk import WebClient
from chat_logger import ChatLoggerHandlerInterface

USER_NAME = os.getenv('APP_NAME', 'y-logger')
TIMEOUT = 5


class SlackHandler(ChatLoggerHandlerInterface):
    def __init__(self, slack_token, channel, **kwargs):
        super().__init__(**kwargs)
        self.slack_token = os.getenv('SLACK_TOKEN') if not slack_token else slack_token
        self.channel = channel
        self.username = USER_NAME
        self.client = WebClient(token=self.slack_token, timeout=TIMEOUT)

    def send_message(self, record):
        message = self.format(record)
        self.client.chat_postMessage(text=message, channel=self.channel, username=self.username)
        return True
