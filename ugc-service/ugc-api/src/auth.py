from json import JSONDecodeError

import httpx
import jwt
from fastapi import HTTPException
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from httpx import Headers
from starlette.requests import Request

from core import config
from core.decorators import backoff_async
from core.exceptions import AuthExceptionError, RetryExceptionError
from core.logger import logger
from db.cache import Cache
from db.redis import get_redis


class CustomHTTPAuthorizationCredentials(HTTPAuthorizationCredentials):
    user_id: str


class TokenCheck(HTTPBearer):
    async def __call__(self, request: Request) -> CustomHTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(httpx.codes.UNAUTHORIZED)
        if config.NO_AUTH:
            return CustomHTTPAuthorizationCredentials(user_id=config.TEST_UUID, **credentials.dict())
        cache_provider = await get_redis()
        cache = Cache(*cache_provider)  # type: ignore
        token = credentials.credentials
        user_id = await cache.get_obj_from_cache(str(token))
        if user_id:
            return CustomHTTPAuthorizationCredentials(user_id=str(user_id), **credentials.dict())
        user_id = jwt.decode(token, options={"verify_signature": False})["sub"]
        request_id = request.headers.get("X-Request-Id") or "none"
        user_roles_resonse = await self.send_request_to_auth(token, request_id)
        if user_roles_resonse is None:
            exception = AuthExceptionError("Auth servier not available")
            logger.exception(exception)
            raise exception
        await cache.put_obj_to_cache(token, user_id)
        return CustomHTTPAuthorizationCredentials(user_id=str(user_id), **credentials.dict())


    @backoff_async(
        logger,
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=10,
        max_retray=2,
    )
    async def send_request_to_auth(self, token: str, request_id: str) -> list:
        async with httpx.AsyncClient() as client:
            headers = Headers(
                {
                    "Host": "Auth",
                    "X-Real-IP": "127.0.0.1",
                    "X-Forwarded-For": "127.0.0.1",
                    "X-Request-Id": request_id,
                }
            )
            try:
                response = await client.post(
                    config.AUTH_URL, headers=headers, json={"access_token": token}
                )
            except httpx.ReadTimeout:
                raise RetryExceptionError("Auth server not available")
            try:
                result = response.json()
            except JSONDecodeError:
                raise RetryExceptionError("Auth server replay not correct")
            if response.status_code in (
                httpx.codes.UNPROCESSABLE_ENTITY,
                httpx.codes.UNAUTHORIZED,
            ):
                raise HTTPException(response.status_code, detail=result)
        return result
