import logging
from app_logging import logger


if __name__ == '__main__':
    logger.debug(f'[{logging.DEBUG}]: Test Message')
    logger.info(f'[{logging.INFO}]: Test Message')
    logger.warning(f'[{logging.WARNING}]: Test Message')
    logger.error(f'[{logging.ERROR}]: Test Message')
    logger.critical(f'[{logging.CRITICAL}]: Test Message')
