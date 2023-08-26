import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://host.docker.internal:27017"  # Подключится в докере без .dev.env

    class Config:
        env_file = ".local.env"


settings = Settings()