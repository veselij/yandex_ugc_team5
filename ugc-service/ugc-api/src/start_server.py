from logging import config as logging_config

import aioredis
import sentry_sdk
import uvicorn
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer
from starlette.middleware import Middleware
from starlette_context import plugins as stalette_plugins
from starlette_context.middleware import RawContextMiddleware

from api.v1.films import router
from core import config
from core.logger_config import LOGGING
from db import kafka, redis

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


@app.on_event("startup")
async def startup():
    redis.redis_client = await aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"
    )
    kafka.kafka_producer = KafkaProducer(
        bootstrap_servers=[f"{config.KAFKA_BROKER_HOST}:{config.KAFKA_BROKER_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(router, prefix="/api/v1", tags=["Films"])

if __name__ == "__main__":
    uvicorn.run(app=app, debug=True, host="127.0.0.1", port=8000)  # type: ignore
