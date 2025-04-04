import logging

from pymongo import MongoClient

from src.core.settings import settings

logger = logging.getLogger(__name__)


def test_mongo_connection():
    try:
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.MONGODB_DATABASE]

        print("Databases:", client.list_database_names())
        print("Collections in DB:", db.list_collection_names())

        print("MongoDB connection successful!")
    except Exception as e:
        print("MongoDB connection failed:", str(e))


if __name__ == "__main__":
    test_mongo_connection()
