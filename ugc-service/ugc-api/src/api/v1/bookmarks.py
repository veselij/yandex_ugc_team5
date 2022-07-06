import datetime
import logging
from typing import Optional
from uuid import uuid4

import motor.motor_asyncio
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, ORJSONResponse
from pymongo.errors import DuplicateKeyError

from auth import TokenCheck
from core.config import logger
from db.mongodb import get_mongo

router = APIRouter()


@router.post('/bookmarks/{movie_id}', status_code=status.HTTP_201_CREATED)
async def create_bookmark(
        movie_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    try:
        result = await mongo.films.bookmarks.insert_one(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "bookmark_id": str(uuid4()),
                "created_at": datetime.datetime.now()}
        )
    except DuplicateKeyError:
        return Response(status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(content={"bookmark_id": result.inserted_id}, status_code=status.HTTP_201_CREATED)


@router.delete('/bookmarks/{movie_id}', status_code=status.HTTP_200_OK)
async def delete_bookmark(
        movie_id: str,
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    await mongo.films.bookmarks.delete_one(
        {"user_id": user_id, "movie_id": movie_id}
    )

    return Response(status_code=status.HTTP_200_OK)


@router.get('/bookmarks/', status_code=status.HTTP_200_OK, response_class=ORJSONResponse)
async def get_bookmarks_by_user(
        user_id: str = Depends(TokenCheck()),
        mongo: motor.motor_asyncio = Depends(get_mongo)
):
    result = await mongo.films.bookmarks.find(
        {"user_id": user_id}, {"_id": 0}
    ).sort("created_at", -1).to_list(length=None)

    return ORJSONResponse(content=result, status_code=status.HTTP_200_OK)
