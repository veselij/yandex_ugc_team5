import datetime
from uuid import uuid4

import motor.motor_asyncio
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.errors import DuplicateKeyError

from auth import TokenCheck
from db.mongodb import get_mongo
from models import Like

router = APIRouter()


@router.post('/like/{movie_id}', status_code=status.HTTP_201_CREATED)
async def create_like(
        movie_id: str,
        like: Like,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    try:
        like_id = str(uuid4())
        result = await mongo.films.likes.insert_one({
            "like_id": like_id,
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": like.rating,
            "created_at": datetime.datetime.now()
        })
    except DuplicateKeyError:
        return Response(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={"like_id": like_id}, status_code=status.HTTP_201_CREATED)


@router.delete('/like/{movie_id}', status_code=status.HTTP_201_CREATED)
async def delete_like(
        movie_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    await mongo.films.likes.delete_one(
        {"movie_id": movie_id, "user_id": user_id}
    )

    return Response(status_code=status.HTTP_200_OK)


@router.get('/like', status_code=status.HTTP_200_OK, response_class=ORJSONResponse)
async def fetch_like_by_user(
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.likes.find(
        {"user_id": user_id}, {"_id": 0}
    ).sort("created_at", -1).to_list(length=None)

    return ORJSONResponse(content=result, status_code=status.HTTP_200_OK)


@router.get('/like/{movie_id}', status_code=status.HTTP_200_OK, response_class=ORJSONResponse)
async def fetch_like_by_user_and_movie(
        movie_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.likes.find_one(
        {"movie_id": movie_id, "user_id": user_id}, {"_id": 0}
    )

    return ORJSONResponse(content=result, status_code=status.HTTP_200_OK)


@router.get('/like-count/{movie_id}', status_code=status.HTTP_200_OK, response_class=ORJSONResponse)
async def fetch_likes_count_by_movie(
        movie_id: str,
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.likes.count_documents({"movie_id": movie_id})

    return ORJSONResponse(content=result, status_code=status.HTTP_200_OK)
