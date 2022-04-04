import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from foodscrape.config import Config

LOGGING_FORMATTER = logging.Formatter(Config.LOGGER_FORMAT, "%Y/%m/%d %H:%M:%S")
LOGGING_FILE = Config.LOGGER_DIR / "scraper.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGING_FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOGGING_FILE, when="midnight")
    file_handler.setFormatter(LOGGING_FORMATTER)
    return file_handler


def get_logger(logger_name) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(Config.LOGGER_LEVEL)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
