import config as app_config
from logging import Handler, LogRecord
from abc import abstractmethod


class ChatLoggerHandlerInterface(Handler):
    def __init__(self, fail_silent=True, stack_trace=True, **kwargs):
        super().__init__()
        self.fail_silent = fail_silent
        self.stack_trace = stack_trace

    @abstractmethod
    def send_message(self, record: LogRecord) -> bool:
        return True

    def emit(self, record):
        if app_config.ENVIRONMENT in app_config.ALLOWED_ENVIRONMENT:
            try:
                self.send_message(record)
            except Exception as e:
                if self.fail_silent:
                    pass
                else:
                    raise e
        else:
            if self.fail_silent:
                pass
            else:
                raise Exception(f'ENVIRONMENT {app_config.ENVIRONMENT} is not allowed under '
                                f'ALLOWED_ENVIRONMENT {app_config.ALLOWED_ENVIRONMENT}\n'
                                f'Please check config file')

    @property
    def allowed_environment(self):
        return {'TESTING', 'STAGING', 'PRODUCTION'}
