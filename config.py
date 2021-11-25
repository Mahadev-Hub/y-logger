from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(override=False)

APP_NAME = os.getenv('APP_NAME', 'y-logger')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'STAGING')
LOG_FILE_INFO = os.getenv('LOG_FILE_INFO', 'info.log')
LOG_FILE_ERROR = os.getenv('LOG_FILE_ERROR', 'error.log')

ALLOWED_ENVIRONMENT = {'STAGING', 'PRODUCTION'}

TIMEOUT = 10
LOG_DIR = Path(__file__).resolve().parent.parent.joinpath('logs')
