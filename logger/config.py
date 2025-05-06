import logging
from logging import StreamHandler

from .custom_handler import MongoDBHandler, AsyncMongoDBHandler
from .settings import LoggerSettings

from datetime import datetime, timezone, timedelta

settings = LoggerSettings()

def kst_converter(*args):
    return datetime.now(timezone(timedelta(hours=9))).timetuple()

def configure_logging(level: str = None, use_async: bool = False):
    log_level_str = level or settings.level
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    formatter.converter = kst_converter

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 기존 핸들러 모두 제거 (중복 방지)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    mongo_handler = AsyncMongoDBHandler() if use_async else MongoDBHandler()
    mongo_handler.setFormatter(formatter)
    root_logger.addHandler(mongo_handler)
