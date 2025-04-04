from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr


class ResetPasswordMessage(BaseModel):
    id: UUID = uuid4()
    user_id: str
    email: EmailStr
    subject: str
    body: str
    published_at: datetime = datetime.now(timezone.utc)
    sent_at: Optional[datetime] = None
