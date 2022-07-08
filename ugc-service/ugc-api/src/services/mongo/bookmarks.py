from fastapi import Depends

from db.mongodb import get_mongo
from services.bookmarks import BaseBookmarkService, Bookmark, Bookmarks, BookmarkDelete, BookmarkGet
from services.mongo.base_mongo import BaseMongoCRUDService
from utils.service_result import ServiceResult


class MongoBookmarksService(BaseBookmarkService, BaseMongoCRUDService):
    async def create(self, item: Bookmark) -> ServiceResult:
        return await self._create(item)

    async def delete(self, item: BookmarkDelete) -> ServiceResult:
        return await self._delete(item)

    async def get_one(self, item: BookmarkGet) -> ServiceResult:
        return await self._get_one(item, Bookmark)

    async def get_list(self, item: BookmarkGet) -> ServiceResult:
        return await self._get_list(item, Bookmarks)


def get_bookmarks_service(db=Depends(get_mongo)):
    return MongoBookmarksService(collection="bookmarks", db=db)
