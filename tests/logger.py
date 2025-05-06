import unittest
import logging
import asyncio
import time

from logger import configure_logging
from logger.database import (
    get_recent_log,
    close_sync_mongo_client,
    close_async_mongo_client
)
from logger.custom_handler import mongo_log_worker, AsyncMongoDBHandler
from .utils import generate_random_string


class TestLogger(unittest.TestCase):
    def tearDown(self):
        """모든 테스트 후 로거 핸들러 초기화 및 클라이언트 종료"""
        logging.shutdown()  # 🔧 flush + close 모든 핸들러
        close_sync_mongo_client()

    def test_sync_logging(self):
        """동기 로깅이 MongoDB에 잘 들어가는지 확인"""
        configure_logging(level="DEBUG", use_async=False)
        logger = logging.getLogger("test_sync_logger")

        random_message = generate_random_string()
        logger.info(random_message)

        # 로그가 MongoDB에 반영될 시간 대기
        for _ in range(10):
            log_entry = get_recent_log(random_message, "test_sync_logger")
            if log_entry:
                break
            time.sleep(0.2)
        else:
            self.fail("Log entry should exist in MongoDB")

        print(f"\n[SYNC] Found log entry: {log_entry}")
        self.assertEqual(log_entry["message"], random_message)
        self.assertEqual(log_entry["logLevel"], "INFO")
        self.assertEqual(log_entry["moduleName"], "test_sync_logger")

    async def _test_async_logging(self):
        """비동기 로깅이 MongoDB에 잘 들어가는지 확인"""
        configure_logging(level="DEBUG", use_async=True)
        logger = logging.getLogger("test_async_logger")

        # 로그 삽입 워커 실행
        worker_task = asyncio.create_task(mongo_log_worker())

        try:
            random_message = generate_random_string()
            logger.info(random_message)

            # 로그 삽입 대기
            await asyncio.sleep(1)

            log_entry = get_recent_log(random_message, "test_async_logger")
            print(f"\n[ASYNC] Found log entry: {log_entry}")
            self.assertIsNotNone(log_entry, "Log entry should exist in MongoDB")
            self.assertEqual(log_entry["message"], random_message)
            self.assertEqual(log_entry["logLevel"], "INFO")
            self.assertEqual(log_entry["moduleName"], "test_async_logger")
        finally:
            # 워커 종료
            worker_task.cancel()
            try:
                await worker_task
            except asyncio.CancelledError:
                pass

            # 핸들러 정리
            for handler in logger.handlers:
                if isinstance(handler, AsyncMongoDBHandler):
                    await handler.close()

            await close_async_mongo_client()

    def test_async_logging(self):
        """비동기 테스트 실행"""
        asyncio.run(self._test_async_logging())


if __name__ == "__main__":
    unittest.main()
