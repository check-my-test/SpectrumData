import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://host.docker.internal:27017"  # Подключится в докере без .dev.env


prefix = os.getenv("ENV_STATE", "local")
settings = Settings(_env_file=f'.{prefix}.env', _env_file_encoding='utf-8')