from motor.motor_asyncio import AsyncIOMotorClient
from config.config import settings

async_client = AsyncIOMotorClient(settings.DATABASE_URL)
db = async_client["parser_db"]
htmls = db["htmls"]
# Создал индекс по уникальному полю url
# В рамках тестового без паролей

async def close_db_connection():
    async_client.close()

