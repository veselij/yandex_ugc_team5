from fastapi import Depends

from db.mongodb import get_mongo
from services.mongo.base_mongo import BaseMongoCRUDService
from services.reviews_likes import BaseReviewLikesService, ReviewLikeCreate, ReviewLikeDelete, ReviewLikeGet, \
    ReviewLike, ReviewLikes
from utils.service_result import ServiceResult


class MongoReviewLikesService(BaseReviewLikesService, BaseMongoCRUDService):
    async def create(self, item: ReviewLikeCreate) -> ServiceResult:
        return await self._create(item)

    async def delete(self, item: ReviewLikeDelete) -> ServiceResult:
        return await self._delete(item)

    async def get_one(self, item: ReviewLikeGet) -> ServiceResult:
        return await self._get_one(item, ReviewLike)

    async def get_list(self, item: ReviewLikeGet) -> ServiceResult:
        return await self._get_list(item, ReviewLikes)


def get_review_likes_service(db=Depends(get_mongo)) -> BaseReviewLikesService:
    return MongoReviewLikesService(collection="reviews_likes", db=db)
