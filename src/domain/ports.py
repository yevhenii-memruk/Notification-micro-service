from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from aio_pika import IncomingMessage

from src.domain.entities import ResetPasswordMessage


class RepositoryPort(ABC):
    @abstractmethod
    async def save(self, message: ResetPasswordMessage) -> UUID:
        pass

    @abstractmethod
    async def update_field(
        self, entity_id: UUID, field_name: str, value: Any
    ) -> bool:
        pass


class ConsumerPort(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def process_message(self, message: IncomingMessage) -> None:
        pass


class EmailSenderPort(ABC):
    @abstractmethod
    async def send_reset_password_email(
        self, message: ResetPasswordMessage
    ) -> None:
        pass
