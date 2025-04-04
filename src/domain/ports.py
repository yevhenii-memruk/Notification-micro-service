from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from src.domain.entities import ResetPasswordMessage


class RepositoryPort(ABC):
    @abstractmethod
    async def save(self, message: ResetPasswordMessage) -> UUID:
        pass

    @abstractmethod
    async def mark_as_sent(self, message_id: UUID, sent_at: datetime) -> bool:
        pass
