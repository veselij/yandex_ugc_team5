from typing import Tuple, Type

from aioredis import ConnectionError, Redis

redis_client: Redis


async def get_redis() -> Tuple[Redis, Type[Exception]]:
    return redis_client, ConnectionError  # noqa: F821
