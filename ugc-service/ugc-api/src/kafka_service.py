from core import config
from db.kafka import get_kafka_producer
from models import FilmWatchTimestamp


async def send_to_kafka(film_timestamp: FilmWatchTimestamp) -> None:
    kafka_producer = await get_kafka_producer()
    key = "{0}+{1}".format(film_timestamp.user_id, film_timestamp.film_id)
    kafka_producer.send(
        topic=config.KAFKA_TOPIC,
        key=key.encode(),
        value=film_timestamp.json().encode(),
    )
