from typing import Type

import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from models import Base
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult


class BaseMongoCRUDService:
    def __init__(self, collection, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        self.collection = db[collection]

    async def _create(self, item: Base) -> ServiceResult:
        try:
            result = await self.collection.insert_one(jsonable_encoder(item, exclude_none=True))
        except DuplicateKeyError:
            return ServiceResult(AppException.AlreadyExistsError())
        if not result.inserted_id:
            return ServiceResult(AppException.UnhandledError())
        return ServiceResult(item)

    async def _delete(self, item: Base) -> ServiceResult:
        result = await self.collection.delete_one(jsonable_encoder(item, exclude_none=True))

        if not result.deleted_count:
            return ServiceResult(AppException.NotFoundError())

        return ServiceResult({})

    async def _get_one(self, item: BaseModel, model: Type[Base]) -> ServiceResult:
        result = await self.collection.find_one(jsonable_encoder(item, exclude_none=True), {"_id": 0})

        if not result:
            return ServiceResult(AppException.NotFoundError())

        return ServiceResult(model(**result))

    async def _get_list(self, item: BaseModel, model: Type[Base]) -> ServiceResult:
        result = await self.collection.find(jsonable_encoder(item, exclude_none=True), {"_id": 0}).to_list(length=None)
        count = await self.collection.count_documents(jsonable_encoder(item, exclude_none=True))
        if not result:
            return ServiceResult(AppException.NotFoundError())

        return ServiceResult(model(items=result, count=count))
