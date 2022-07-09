from typing import Type, Tuple

from aioredis import Redis, ConnectionError

redis_client: Redis


async def get_redis() -> Tuple[Redis, Type[Exception]]:
    return redis_client, ConnectionError
