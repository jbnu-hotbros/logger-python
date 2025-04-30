import logging
from logging import StreamHandler

from app.config import MODULE_NAME
from app.logger.database_handler import MongoDBHandler

_logger = None

def get_logger():
    global _logger
    if _logger is not None:
        return _logger

    logger = logging.getLogger(MODULE_NAME)
    logger.setLevel(logging.DEBUG)
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