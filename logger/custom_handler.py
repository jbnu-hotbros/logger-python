import sys
import logging
import asyncio
from typing import Optional
from datetime import datetime, timezone, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from .database import get_sync_mongo_client, get_async_mongo_client, close_async_mongo_client

# --- 비동기 로깅 큐 ---
log_queue: asyncio.Queue = asyncio.Queue()

# --- 공통 KST 변환 유틸 ---
KST = timezone(timedelta(hours=9))

def to_kst_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=KST)

# --- 필터 클래스 ---
class ExcludeInternalLogsFilter(logging.Filter):
    BLOCKED_PREFIXES = (
        "pymongo", "motor", "asyncio", "uvicorn", "concurrent",
        "httpcore", "httpx", "urllib3", "starlette"
    )

    def filter(self, record: logging.LogRecord) -> bool:
        return not record.name.startswith(self.BLOCKED_PREFIXES)

# --- 동기 MongoDB 핸들러 ---
class MongoDBHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.client: MongoClient = get_sync_mongo_client()
        self.collection = self.client["log"]["log"]
        self.addFilter(ExcludeInternalLogsFilter())  # 필터 추가

    def emit(self, record: logging.LogRecord):
        try:
            log_entry = self._format_log_entry(record)
            self.collection.insert_one(log_entry)
        except Exception as e:
            print("MongoDBHandler insert failed:", e, file=sys.stderr)

    def _format_log_entry(self, record: logging.LogRecord) -> dict:
        return {
            "moduleName": record.name,
            "functionLocation": f"{record.pathname}:{record.funcName}:{record.lineno}",
            "timestamp": to_kst_datetime(record.created),
            "logLevel": record.levelname,
            "message": record.getMessage(),
        }

    def close(self):
        try:
            self.client.close()
            print("MongoDBHandler: Mongo Client is closed.")
        except Exception as e:
            print("MongoDBHandler: MongoClient close failed:", e)

# --- 비동기 MongoDB 핸들러 ---
class AsyncMongoDBHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.client: AsyncIOMotorClient = get_async_mongo_client()
        self.collection = self.client["log"]["log"]
        self._closed = False
        self.addFilter(ExcludeInternalLogsFilter())  # 필터 추가

    def emit(self, record: logging.LogRecord):
        try:
            log_entry = self._format_log_entry(record)
            log_queue.put_nowait(log_entry)
        except Exception as e:
            print("AsyncMongoDBHandler emit failed:", e, file=sys.stderr)

    def _format_log_entry(self, record: logging.LogRecord) -> dict:
        return {
            "moduleName": record.name,
            "functionLocation": f"{record.pathname}:{record.funcName}:{record.lineno}",
            "timestamp": to_kst_datetime(record.created),
            "logLevel": record.levelname,
            "message": record.getMessage(),
        }

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(close_async_mongo_client())
            else:
                loop.run_until_complete(close_async_mongo_client())
        except Exception as e:
            print("AsyncMongoDBHandler: Error during close:", e, file=sys.stderr)

# --- 비동기 로그 삽입 워커 ---
async def mongo_log_worker(client: Optional[AsyncIOMotorClient] = None):
    client = client or get_async_mongo_client()
    collection = client["log"]["log"]

    while True:
        try:
            log_entry = await log_queue.get()
            await collection.insert_one(log_entry)
        except Exception as e:
            print("Async Mongo log insert failed:", e, file=sys.stderr)
