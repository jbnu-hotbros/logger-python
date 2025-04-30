import os
import pymongo

from app.config import (
    LOGGER_MONGO_DATABASE_HOST,
    LOGGER_MONGO_DATABASE_PORT,
    LOGGER_MONGO_DATABASE_ID,
    LOGGER_MONGO_DATABASE_PASSWORD
)

def get_uri():
    return f"mongodb://{LOGGER_MONGO_DATABASE_ID}:{LOGGER_MONGO_DATABASE_PASSWORD}@{LOGGER_MONGO_DATABASE_HOST}:{LOGGER_MONGO_DATABASE_PORT}"

def get_mongo_client():
    uri = get_uri()
    return pymongo.MongoClient(uri)

def get_recent_log(message: str, module_name: str = None):
    """
    최근 MongoDB 로그 중 지정된 메시지를 포함한 가장 최신 로그를 반환
    """

    client = get_mongo_client()
    collection = client["log"]["log"]

    query = {"message": message}
    if module_name:
        query["moduleName"] = module_name

    ret = collection.find_one(query, sort=[("timestamp", -1)])

    client.close()
    
    return ret
