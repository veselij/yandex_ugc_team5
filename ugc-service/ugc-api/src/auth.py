import httpx
from fastapi import HTTPException
from fastapi.security.http import HTTPBearer
from starlette.requests import Request

from core import config
from core.decorators import backoff_async
from core.exceptions import AuthExceptionError, RetryExceptionError
from db.cache import Cache
from db.redis import get_redis


class TokenCheck(HTTPBearer):
    async def __call__(self, request: Request) -> bool:
        credentials = await super().__call__(request)
        if not credentials:
            return False
        if config.NO_AUTH:
            return True
        cache_provider = await get_redis()
        cache = Cache(*cache_provider)   # type: ignore
        token = credentials.credentials
        if await cache.get_obj_from_cache(str(token)):
            return True
        else:
            user_roles_resonse = await self.send_request_to_auth(token)
            if user_roles_resonse is None:
                exception = AuthExceptionError("Auth servier not available")
                config.logging.exception(exception)
                raise exception
            await cache.put_obj_to_cache(token, "token")
            return True

    @backoff_async(
        config.logger,
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=10,
        max_retray=2,
    )
    async def send_request_to_auth(self, token: str) -> list:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    config.AUTH_URL, json={"access_token": token}
                )
            except httpx.ReadTimeout:
                raise RetryExceptionError("Auth server not available")
            result = response.json()
            if response.status_code in (
                httpx.codes.UNPROCESSABLE_ENTITY,
                httpx.codes.UNAUTHORIZED,
            ):
                raise HTTPException(response.status_code, detail=result)
        return result
