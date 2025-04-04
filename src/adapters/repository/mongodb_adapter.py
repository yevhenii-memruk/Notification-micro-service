import logging
from datetime import datetime
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from src.core.settings import settings
from src.domain.entities import ResetPasswordMessage

logger = logging.getLogger(__name__)


class MongoDBAdapter:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client[settings.MONGODB_DATABASE]
        self.collection = self.db["reset_password_messages"]
        logger.info("Connected to MongoDB.")

    async def save(self, message: ResetPasswordMessage) -> UUID:
        """Insert a reset password message into MongoDB."""
        message_dict = message.model_dump()
        try:
            await self.collection.insert_one(message_dict)
            return message.id
        except PyMongoError as e:
            logger.error(f"MongoDB Insert Error: {e}")
            raise e

    async def mark_as_sent(self, message_id: UUID, sent_at: datetime) -> bool:
        """Update sent_at timestamp for the message."""
        try:
            result = await self.collection.update_one(
                {"id": str(message_id)}, {"$set": {"sent_at": sent_at}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            logger.error(f"MongoDB Update Error: {e}")
            raise e
