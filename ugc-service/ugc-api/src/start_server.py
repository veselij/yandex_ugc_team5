from logging import config as logging_config

import aioredis
import motor.motor_asyncio
import sentry_sdk
import uvicorn
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer
from starlette.middleware import Middleware
from starlette_context import plugins as stalette_plugins
from starlette_context.middleware import RawContextMiddleware

from api.v1.bookmarks import router as bookmarks
from api.v1.films import router as player_progress
from api.v1.likes import router as likes
from api.v1.reviews import router as reviews
from api.v1.reviews_likes import router as reviews_likes
from core import config
from core.logger_config import LOGGING
from db import kafka, mongodb, redis
from utils.app_exceptions import AppExceptionCaseError, app_exception_handler

sentry_sdk.init(dsn=config.SENTRY_DSN, traces_sample_rate=1)
request_id_middleware = Middleware(
    RawContextMiddleware, plugins=(stalette_plugins.RequestIdPlugin(),)
)

logging_config.dictConfig(LOGGING)
app = FastAPI(
    title=config.PROJECT_NAME,
    description="API service for receiving film watch timestamp",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    middleware=[request_id_middleware],
)


@app.exception_handler(AppExceptionCaseError)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.on_event("startup")
async def startup():
    mongodb.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)
    redis.redis_client = await aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"
    )
    kafka.kafka_producer = KafkaProducer(
        bootstrap_servers=[f"{config.KAFKA_BROKER_HOST}:{config.KAFKA_BROKER_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(player_progress, prefix="/api/v1", tags=["Films"])
app.include_router(bookmarks, prefix="/api/v1", tags=["Bookmarks"])
app.include_router(reviews, prefix="/api/v1", tags=["Reviews"])
app.include_router(likes, prefix="/api/v1", tags=["Likes"])
app.include_router(reviews_likes, prefix="/api/v1", tags=["Revies", "Likes"])

if __name__ == "__main__":
    uvicorn.run(app=app, debug=True, host="localhost", port=8000)  # type: ignore
