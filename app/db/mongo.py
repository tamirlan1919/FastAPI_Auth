from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings


def create_mongo_client():
    client = AsyncMongoClient(
        settings.mongo_url,
        tz_aware=True,
        serverSelectionTimeoutMS=5000,
    )
    return client


client = create_mongo_client()
database = client[settings.mongo_db]


def get_database() -> AsyncIOMotorDatabase:
    return database


