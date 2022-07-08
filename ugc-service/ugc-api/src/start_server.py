import aioredis
import motor.motor_asyncio
import uvicorn
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer

from api.v1.bookmarks import router as bookmarks
from api.v1.films import router as player_progress
from api.v1.likes import router as likes
from api.v1.reviews import router as reviews
from api.v1.reviews_likes import router as reviews_likes
from core import config
from db import kafka, redis, mongodb
from utils.app_exceptions import app_exception_handler, AppExceptionCase

app = FastAPI(
    title=config.PROJECT_NAME,
    description="API service for receiving film watch timestamp",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.exception_handler(AppExceptionCase)
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
    uvicorn.run(app=app, debug=True, host="0.0.0.0", port=8000)  # type: ignore
