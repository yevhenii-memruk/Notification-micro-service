from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

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
