import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


async_client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = async_client["parser_db"]
htmls = db["htmls"]
# Создал индекс по уникальному полю url

async def close_db_connection():
    async_client.close()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    # @classmethod
    # def __get_pydantic_json_schema__(cls, field_schema):
    #     field_schema.update(type="string")
