from aiokafka import AIOKafkaProducer
import json
import logging

from app.core.config import config

logger = logging.getLogger(__name__)

producer: AIOKafkaProducer | None = None


async def init_kafka() -> None:
    global producer
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        )
        await producer.start()
        logger.info("Kafka producer connected successfully.")
    except Exception as e:
        logger.warning(f"⚠️ Kafka connection failed: {e}. Running without event publishing.")
        producer = None


async def close_kafka() -> None:
    global producer
    if producer:
        await producer.stop()
        producer = None


async def publish_event(
    topic: str,
    event: dict,
) -> None:
    if producer is None:
        logger.warning(f"Kafka producer is offline. Skipping event for topic: {topic}")
        return

    await producer.send_and_wait(
        topic,
        json.dumps(event).encode("utf-8"),
    )