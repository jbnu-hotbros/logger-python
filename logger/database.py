import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from logger.settings import settings

# 내부 URI 생성 함수
def _get_uri() -> str:
    return f"mongodb://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"

# --- 동기 클라이언트 싱글턴 ---
_sync_client: pymongo.MongoClient | None = None

def get_sync_mongo_client() -> pymongo.MongoClient:
    global _sync_client
    if _sync_client is None:
        _sync_client = pymongo.MongoClient(_get_uri())
    return _sync_client

# --- 비동기 클라이언트 싱글턴 ---
_async_client: AsyncIOMotorClient | None = None

def get_async_mongo_client() -> AsyncIOMotorClient:
    global _async_client
    if _async_client is None:
        _async_client = AsyncIOMotorClient(_get_uri())
    return _async_client

async def close_async_mongo_client():
    global _async_client
    if _async_client is not None:
        _async_client.close()
        _async_client = None

def close_sync_mongo_client():
    global _sync_client
    if _sync_client is not None:
        _sync_client.close()
        _sync_client = None

# --- 유틸 함수: 최근 로그 1개 가져오기 ---
def get_recent_log(message: str, module_name: str = None):
    client = get_sync_mongo_client()
    collection = client["log"]["log"]

    query = {"message": message}
    if module_name:
        query["moduleName"] = module_name

    return collection.find_one(query, sort=[("timestamp", -1)])
