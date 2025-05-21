import asyncio
import logging

from src.adapters.message_broker.consumer import Consumer
from src.core.logger import configure_logger
from src.core.settings import settings

logger = logging.getLogger("main")


async def main():
    configure_logger()
    consumer = Consumer(queue_name=settings.RABBITMQ_QUEUE)
    await consumer.connect()
    logger.info("Consumer is running. Waiting for messages")
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down service")
