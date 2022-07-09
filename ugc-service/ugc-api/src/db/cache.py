import platform
from typing import Optional, Type

if platform.python_version_tuple()[:2] == (3, 7):
    from typing_extensions import Protocol
else:
    from typing import Protocol  # type:ignore

from core.decorators import backoff_async
from core.exceptions import RetryExceptionError
from core.logger import logger


class AbstractCache(Protocol):
    async def get(self, name: str) -> Optional[bytes]:
        ...

    async def set(self, name: str, value: str, ex: int) -> Optional[bool]:
        ...


class Cache:
    cache_timer = 60 * 5

    def __init__(self, cache: AbstractCache, exc: Type[Exception]) -> None:
        self.cache = cache
        self.exc = exc

    @backoff_async(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
    async def get_obj_from_cache(self, obj_id: str) -> Optional[bytes]:
        try:
            data = await self.cache.get(obj_id)
        except self.exc:
            raise RetryExceptionError("cache not available")

        if not data:
            return None
        return data

    @backoff_async(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
    async def put_obj_to_cache(self, key: str, obj: str) -> None:
        try:
            await self.cache.set(key, obj, ex=self.cache_timer)
        except self.exc:
            raise RetryExceptionError("cache not available")
