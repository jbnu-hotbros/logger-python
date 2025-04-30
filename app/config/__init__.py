import os
import dotenv

# override=True로 설정하여 기존 환경변수를 덮어씁니다
dotenv.load_dotenv(override=True)

MODULE_NAME = os.getenv("MODULE_NAME", "unknown")
LOGGER_MONGO_DATABASE_HOST=os.getenv("LOGGER_MONGO_DATABASE_HOST", "127.0.0.1")
LOGGER_MONGO_DATABASE_PORT=os.getenv("LOGGER_MONGO_DATABASE_PORT", 27017)
LOGGER_MONGO_DATABASE_ID=os.getenv("LOGGER_MONGO_DATABASE_ID", "root")
LOGGER_MONGO_DATABASE_PASSWORD=os.getenv("LOGGER_MONGO_DATABASE_PASSWORD", "rootpw")
