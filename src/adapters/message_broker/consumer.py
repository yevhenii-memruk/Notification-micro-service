import json
import logging

from aio_pika import IncomingMessage, connect_robust
from aio_pika.abc import AbstractQueue

from src.core.settings import settings
from src.dependencies import get_send_reset_password_use_case
from src.domain.ports import ConsumerPort

logger = logging.getLogger(__name__)


class Consumer(ConsumerPort):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.use_case = get_send_reset_password_use_case()

    async def connect(self):
        self.connection = await connect_robust(settings.rabbitmq_uri)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

        queue: AbstractQueue = await self.channel.declare_queue(
            self.queue_name, durable=True
        )
        await queue.consume(self.process_message)

        logger.info(f"Consuming messages from queue: {self.queue_name}")

    async def process_message(self, message: IncomingMessage):
        headers = message.headers or {}
        retry_count = 0

        x_death = headers.get("x-death", [])
        if x_death and isinstance(x_death, list):
            retry_count = x_death[0].get("count", 0)

        try:
            payload = json.loads(message.body.decode())
            logger.debug(f"Received message (retry={retry_count}): {payload}")

            await self.use_case.execute(payload)

            await message.ack()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

            if retry_count >= 5:
                logger.warning("Max retry count exceeded. Sending to DLQ.")
                await message.reject(requeue=False)
            else:
                logger.info("Retrying message")
                await message.nack(requeue=True)
