from fastapi import Depends

from db.mongodb import get_mongo
from services.likes import (
    BaseLikesService,
    Like,
    LikeDelete,
    LikeGet,
    Likes,
)
from services.mongo.base_mongo import BaseMongoCRUDService
from utils.service_result import ServiceResult


class MongoLikesService(BaseLikesService, BaseMongoCRUDService):
    async def create(self, item: Like) -> ServiceResult:
        return await self._create(item)

    async def delete(self, item: LikeDelete) -> ServiceResult:
        return await self._delete(item)

    async def get_one(self, item: LikeGet) -> ServiceResult:
        return await self._get_one(item, Like)

    async def get_list(self, item: LikeGet) -> ServiceResult:
        return await self._get_list(item, Likes)


def get_likes_service(db=Depends(get_mongo)):
    return MongoLikesService(collection="movies_likes", db=db)
