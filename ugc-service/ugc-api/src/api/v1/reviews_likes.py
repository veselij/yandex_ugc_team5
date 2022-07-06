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


class RatingEnum(IntEnum):
    like = 0
    dislike = 10


class ReviewLike(BaseModel):
    rating: RatingEnum


@router.post('/review/{review_id}/like', status_code=status.HTTP_201_CREATED)
async def create_like(
        review_id: str,
        like: ReviewLike,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    try:
        like_id = str(uuid4())
        result = await mongo.films.likes.insert_one({
            "like_id": like_id,
            "user_id": user_id,
            "review_id": review_id,
            "rating": like.rating,
            "created_at": datetime.datetime.now()
        })
    except DuplicateKeyError:
        return Response(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={"like_id": like_id}, status_code=status.HTTP_201_CREATED)


@router.delete('/review/{review_id}/like', status_code=status.HTTP_201_CREATED)
async def delete_like(
        review_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    await mongo.films.likes.delete_one(
        {"review_id": review_id, "user_id": user_id}
    )

    return Response(status_code=status.HTTP_200_OK)


@router.get('/review/{review_id}/like-count', status_code=status.HTTP_200_OK, response_class=ORJSONResponse)
async def fetch_likes_count_by_movie(
        review_id: str,
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.likes.count_documents({"review_id": movie_id})

    return ORJSONResponse(content=result, status_code=status.HTTP_200_OK)
