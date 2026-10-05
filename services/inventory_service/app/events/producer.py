from aiokafka import AIOKafkaProducer
import json

from app.core.config import config


producer: AIOKafkaProducer | None = None


async def init_kafka() -> None:
    global producer

    producer = AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
    )

    await producer.start()


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
        raise RuntimeError(
            "Kafka producer is not initialized"
        )

    await producer.send_and_wait(
        topic,
        json.dumps(event).encode("utf-8"),
    )