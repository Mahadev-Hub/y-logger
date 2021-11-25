from chat_logger import ChatLoggerHandlerInterface


class DiscordHandler(ChatLoggerHandlerInterface):
    def __init__(self, discord_token, channel, **kwargs):
        super().__init__(**kwargs)

    def send_message(self, record):
        return
