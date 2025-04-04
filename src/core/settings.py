from typing import Literal, TypeAlias

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env", raise_error_if_not_found=True)
    )

    # Project
    PROJECT_NAME: str = "Notification-micro-service"
    DEBUG: bool = False
    LOG_LEVEL: LogLevel = "INFO"
    LOG_DIR: str = "logs"

    # RabbitMQ
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_URI: str
    RABBITMQ_QUEUE: str = "reset-password-stream"
    RABBITMQ_RETRY_LIMIT: int = 5

    # MongoDB
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_ROOT_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_DATABASE: str
    MONGODB_ROOT_USERNAME: str

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    EMAIL_SENDER: str

    @property
    def mongodb_uri(self) -> str:
        return (
            f"mongodb://"
            f"{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@"
            f"{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DATABASE}"
        )


settings = Settings()
