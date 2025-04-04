import logging
from typing import Any
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from src.domain.entities import ResetPasswordMessage
from src.domain.ports import RepositoryPort

logger = logging.getLogger(__name__)


class MessageRepository(RepositoryPort):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        db_name: str,
        collection_name: str = "reset_password_messages",
    ):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
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

    async def update_field(
        self, entity_id: UUID, field_name: str, value: Any
    ) -> bool:
        """Update sent_at timestamp for the message."""
        try:
            result = await self.collection.update_one(
                {"id": str(entity_id)}, {"$set": {field_name: value}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            logger.error(f"MongoDB Update Error: {e}")
            raise e
