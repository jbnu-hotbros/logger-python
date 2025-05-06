from pydantic_settings import BaseSettings

class LoggerSettings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = "root"
    mongo_password: str = "password"
    level: str = "INFO"

    class Config:
        env_file = ".env"
        env_prefix = "LOGGER_"

settings = LoggerSettings()