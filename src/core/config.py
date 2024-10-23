from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    DEBUG: bool = Field(default=1, env='DEBUG')

    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_DAYS:  int = Field(..., env='ACCESS_TOKEN_EXPIRE_DAYS')
    REFRESH_TOKEN_EXPIRE_DAYS:  int = Field(..., env='REFRESH_TOKEN_EXPIRE_DAYS')

    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')

    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    POSTGRES_PORT: str = Field(..., env='POSTGRES_PORT')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field(..., env='POSTGRES_DB')

    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    TELEGRAM_BOT_USERNAME: str = Field(..., env='TELEGRAM_BOT_USERNAME')
    TELEGRAM_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env='TELEGRAM_ACCESS_TOKEN_EXPIRE_MINUTES')

    MESSANGER_API_BASE_URL: str = Field(..., env='MESSANGER_API_BASE_URL')

    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: str = Field(..., env='REDIS_PORT')
    REDIS_DB: str = Field(..., env='REDIS_DB')

    class Config:
        env_file = '.env'


settings = Settings()
