import logging
from logging import StreamHandler

from .custom_handler import MongoDBHandler, AsyncMongoDBHandler, ExcludeInternalLogsFilter
from .settings import LoggerSettings

from datetime import datetime, timezone, timedelta

settings = LoggerSettings()

def kst_converter(*args):
    return datetime.now(timezone(timedelta(hours=9))).timetuple()

def configure_logging(level: str = None, use_streamhandler: bool = False, use_async: bool = False, internal_filter: bool = False):
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

    # 필터 생성
    internal_filter = ExcludeInternalLogsFilter()

    # 스트림 핸들러 설정
    if use_streamhandler:
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        if internal_filter:
            stream_handler.addFilter(internal_filter)  # 필터 추가
        root_logger.addHandler(stream_handler)

    # MongoDB 핸들러 설정
    mongo_handler = AsyncMongoDBHandler() if use_async else MongoDBHandler()
    mongo_handler.setFormatter(formatter)
    root_logger.addHandler(mongo_handler)
