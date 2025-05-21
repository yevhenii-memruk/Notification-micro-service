from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.domain.entities import ResetPasswordMessage
from src.domain.ports import EmailSenderPort, RepositoryPort


class SendResetPasswordUseCase:
    def __init__(
        self,
        email_sender: EmailSenderPort,
        repository: RepositoryPort,
        mongo_client: AsyncIOMotorClient,
        db_name: str,
    ):
        self.email_sender = email_sender
        self.repository = repository
        self.client = mongo_client
        self.db: AsyncIOMotorDatabase = self.client[db_name]

    async def execute(self, message_data: dict) -> None:
        message = ResetPasswordMessage(**message_data)

        async with await self.client.start_session() as session:
            async with session.start_transaction():
                # Save message to MongoDB
                await self.repository.save(message)

                # Try to send email
                try:
                    await self.email_sender.send_reset_password_email(message)
                except Exception as e:
                    raise RuntimeError(f"Email sending failed: {e}")
