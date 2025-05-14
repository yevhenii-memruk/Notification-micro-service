import logging

import aioboto3
from botocore.exceptions import ClientError

from src.domain.entities import ResetPasswordMessage
from src.domain.ports import EmailSenderPort

logger = logging.getLogger(__name__)


class AWSEmailSender(EmailSenderPort):
    def __init__(self, aws_region: str, sender_email: str):
        self.aws_region = aws_region
        self.sender_email = sender_email

    async def send_reset_password_email(
        self, message: ResetPasswordMessage
    ) -> None:
        async with aioboto3.client(
            "ses", region_name=self.aws_region
        ) as client:
            try:
                await client.send_email(
                    Source=self.sender_email,
                    Destination={"ToAddresses": [message.email]},
                    Message={
                        "Subject": {"Data": message.subject},
                        "Body": {"Text": {"Data": message.body}},
                    },
                )
                logger.info(f"Reset password email sent to {message.email}")
            except ClientError as e:
                logger.error(f"Failed to send email via AWS SES: {e}")
                raise
