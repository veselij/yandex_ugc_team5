import datetime
from typing import Optional
from uuid import uuid4

import motor.motor_asyncio
from fastapi import APIRouter, status, Depends
from fastapi.responses import Response, ORJSONResponse
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from auth import TokenCheck
from db.mongodb import get_mongo

router = APIRouter()


class Review(BaseModel):
    text: str


@router.post(
    '/review/{movie_id}',
    status_code=status.HTTP_201_CREATED, response_class=ORJSONResponse
)
async def create_review(
        movie_id: str,
        review: Review,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    try:
        review_id = str(uuid4())
        result = await mongo.films.reviews.insert_one({
            "review_id": review_id,
            "user_id": user_id,
            "movie_id": movie_id,
            "text": review.text,
            "created_at": datetime.datetime.now()
        })
    except DuplicateKeyError:
        return Response(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={"review_id": review_id}, status_code=status.HTTP_201_CREATED)


@router.get(
    '/review/{movie_id}/user',
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse
)
async def fetch_by_user_and_movie(
        movie_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.reviews.find_one({
        "user_id": user_id,
        "movie_id": movie_id,
    }, {"_id": 0})

    return ORJSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@router.get(
    '/review',
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse
)
async def fetch_by_user(
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.reviews.find({
        "user_id": user_id,
    }, {"_id": 0}).sort("created_at", -1).to_list(length=None)

    return ORJSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@router.get(
    '/review/{movie_id}',
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse
)
async def fetch_by_movie(
        movie_id: str,
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.reviews.find({
        "movie_id": movie_id,
    }, {"_id": 0}).sort("created_at", -1).to_list(length=None)

    return ORJSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@router.delete(
    '/review/{movie_id}',
    status_code=status.HTTP_201_CREATED
)
async def delete_review(
        movie_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    await mongo.films.reviews.delete_one(
        {"user_id": user_id, "movie_id": movie_id}
    )

    return Response(status_code=status.HTTP_200_OK)
