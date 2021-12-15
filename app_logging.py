import os
from pathlib import Path
import config as app_config
import logging
from logging import config as logging_config

app_logging_config = {
    'version': 1,
    'loggers': {
        app_config.APP_NAME: {
            'level': 'NOTSET',
            'handlers': ['console',
                         'info_file_handler',
                         'error_file_handler',
                         # 'fluent_async_handler',
                         'slack_error',
                         'slack_info',
                         ],
        },
        'gunicorn.access': {  # gunicorn default access logger
            'level': 'NOTSET',
            'handlers': [
                'console',
                'info_file_handler',
                # 'fluent_async_handler',
                'slack_info'
            ],
        },
        'gunicorn.error': {  # gunicorn default error logger
            'level': 'NOTSET',
            'handlers': [
                'console',
                'error_file_handler',
                # 'fluent_async_handler',
                'slack_error',
            ],
        },
    },
    'handlers': {
        'console': {
            'level': os.getenv('LOG_LEVEL', 'DEBUG'),
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_file_handler': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(Path(app_config.LOG_DIR).joinpath(app_config.LOG_FILE_INFO)),
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': os.getenv('LOG_LEVEL', 'ERROR'),
            'formatter': 'error',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(Path(app_config.LOG_DIR).joinpath(app_config.LOG_FILE_ERROR)),
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'fluent_async_handler': {
            'level': os.getenv('LOG_LEVEL', 'CRITICAL'),
            'class': 'fluent.handler.FluentHandler',
            'host': 'localhost',
            'port': 24224,
            'tag': f'{app_config.APP_NAME}.{app_config.ENVIRONMENT}.{os.getenv("REGION", "IND")}',
            'buffer_overflow_handler': 'overflow_handler',
            'formatter': 'night_watch'
        },
        # Slack logger affects the application performance, make sure you keep the right LOG_LEVEL
        # It basically sends api request to slack via http
        'slack_info': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),  # ERROR level is recommended
            'formatter': 'info',
            'class': 'chat_logger.slack.slack_handler.SlackHandler',
            'channel': os.getenv('SLACK_INFO_CHANNEL', '#slack-info'),
            'slack_token': os.getenv('SLACK_TOKEN'),
            'fail_silent': True,
            'stack_trace': True
        },
        # Slack logger affects the application performance, make sure you keep the right LOG_LEVEL
        # It basically sends api request to slack via http
        'slack_error': {
            'level': os.getenv('LOG_LEVEL', 'ERROR'),  # CRITICAL level is recommended
            'formatter': 'error',
            'class': 'chat_logger.slack.slack_handler.SlackHandler',
            'channel': os.getenv('SLACK_ERROR_CHANNEL', '#slack-error'),
            'slack_token': os.getenv('SLACK_TOKEN'),
            'fail_silent': True,
            'stack_trace': True
        },
    },
    'formatters': {
        'info': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(module)s-%(lineno)s:: %(message)s'
        },
        'error': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(module)s-%(lineno)s:: %(message)s'
        },
        'night_watch': {
            '()': 'fluent.handler.FluentRecordFormatter',
            'format': {
                'time': '%(asctime)s',
                'level': '%(levelname)s',
                'hostname': '%(hostname)s',
                'where': '%(name)s-%(module)s-%(lineno)s',
            }
        }
    },
}

app_logging_config["formatters"]["night_watch"]["format"]["hostname"] = \
    app_logging_config["handlers"]["fluent_async_handler"]["tag"]

logging_config.dictConfig(app_logging_config)
logger = logging.getLogger(app_config.APP_NAME)
logger.info("[FIRST LOG]: Logger ready")
