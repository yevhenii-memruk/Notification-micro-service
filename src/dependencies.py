from motor.motor_asyncio import AsyncIOMotorClient

from src.adapters.email_sender.ses_adapter import AWSEmailSender
from src.adapters.repository.message_repository import MessageRepository
from src.application.services import SendResetPasswordUseCase
from src.core.settings import settings


def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.mongodb_uri)


def get_send_reset_password_use_case() -> SendResetPasswordUseCase:
    mongo_client = get_mongo_client()
    repository = MessageRepository(
        client=mongo_client,
        db_name=settings.MONGODB_DATABASE,
        collection_name="reset_password_messages",
    )
    email_sender = AWSEmailSender(
        aws_region=settings.AWS_REGION,
        sender_email=settings.EMAIL_SENDER,
    )
    return SendResetPasswordUseCase(
        email_sender=email_sender,
        repository=repository,
        mongo_client=mongo_client,
        db_name=settings.MONGODB_DATABASE,
    )
