from fastapi import Depends

from db.mongodb import get_mongo
from services.mongo.base_mongo import BaseMongoCRUDService
from services.reviews import BaseReviewsService, Review, Reviews, ReviewDelete, ReviewGetPublic
from utils.service_result import ServiceResult


class MongoReviewsService(BaseReviewsService, BaseMongoCRUDService):
    async def create(self, item: Review) -> ServiceResult:
        return await self._create(item)

    async def delete(self, item: ReviewDelete) -> ServiceResult:
        return await self._delete(item)

    async def get_one(self, item: ReviewGetPublic) -> ServiceResult:
        return await self._get_one(item, Review)

    async def get_list(self, item: ReviewGetPublic) -> ServiceResult:
        return await self._get_list(item, Reviews)


def get_reviews_service(db=Depends(get_mongo)):
    return MongoReviewsService(collection="reviews", db=db)
