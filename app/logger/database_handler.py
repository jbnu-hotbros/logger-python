import sys
import logging

import atexit

import inspect

from app.logger.database import get_mongo_client
from app.utils.time import get_current_time

from app.config import MODULE_NAME

class MongoDBHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.client = get_mongo_client()
        self.database = self.client["log"]
        self.collection = self.database["log"]

        atexit.register(self.cleanup)
        
    def emit(self, record: logging.LogRecord):
        frame = inspect.currentframe().f_back.f_back
        
        log_entry = {
            "moduleName": MODULE_NAME,
            "functionLocation": f"{record.pathname}:{record.funcName}:{record.lineno}",
            "timestamp": get_current_time(),
            "logLevel": record.levelname,
            "message": record.getMessage()
        }

        try:
            self.collection.insert_one(log_entry)
        except Exception as e:
            print("MongoDBHandler insert failed:", e, file=sys.stderr)

    def cleanup(self):
        try:
            self.client.close()
            print("MongoDBHandler: Mongo Client is closed.")
        except Exception as e:
            print("MongoDBHandler: MongoClient close failed:", e)