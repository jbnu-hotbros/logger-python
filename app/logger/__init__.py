import logging
from logging import StreamHandler

from app.config import MODULE_NAME, MINIMUM_LOG_LEVEL
from app.logger.database_handler import MongoDBHandler

_logger = None

try:
    minimum_log_level = int(MINIMUM_LOG_LEVEL)
except ValueError:
    MINIMUM_LOG_LEVEL = MINIMUM_LOG_LEVEL.upper()
    if MINIMUM_LOG_LEVEL == "DEBUG":
        minimum_log_level = logging.DEBUG
    elif MINIMUM_LOG_LEVEL == "INFO":
        minimum_log_level = logging.INFO
    elif MINIMUM_LOG_LEVEL == "WARNING":
        minimum_log_level = logging.WARNING
    elif MINIMUM_LOG_LEVEL == "ERROR":
        minimum_log_level = logging.ERROR
    else:
        minimum_log_level = logging.CRITICAL

def get_logger():
    global _logger
    if _logger is not None:
        return _logger

    logger = logging.getLogger(MODULE_NAME)
    logger.setLevel(minimum_log_level)
    logger.propagate = False

    if not logger.handlers:
        # stdout handler
        stream_handler = StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s:%(lineno)d | %(message)s"
        ))
        logger.addHandler(stream_handler)

        # MongoDB handler
        mongo_handler = MongoDBHandler()
        logger.addHandler(mongo_handler)

    _logger = logger
    return _logger