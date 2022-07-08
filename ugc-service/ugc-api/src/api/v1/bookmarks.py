from uuid import UUID

from fastapi import APIRouter, Depends

from auth import TokenCheck
from services.bookmarks import Bookmark, BaseBookmarkService, BookmarkDelete, BookmarkGet, \
    Bookmarks, BookmarkCreate
from services.mongo.bookmarks import get_bookmarks_service
from utils.service_result import handle_result

router = APIRouter()


@router.post('/bookmarks', response_model=Bookmark)
async def create(
        bookmark: BookmarkCreate,
        user_id: UUID = Depends(TokenCheck()),
        service: BaseBookmarkService = Depends(get_bookmarks_service)
):
    return handle_result(await service.create(item=Bookmark(
        movie_id=bookmark.movie_id,
        user_id=user_id
    )))


@router.delete('/bookmarks/{bookmark_id}')
async def delete(
        bookmark_id: UUID,
        user_id: UUID = Depends(TokenCheck()),
        service: BaseBookmarkService = Depends(get_bookmarks_service)
):
    return handle_result(await service.delete(item=BookmarkDelete(
        bookmark_id=bookmark_id,
        user_id=user_id,
    )))


@router.get('/bookmarks/{bookmark_id}', response_model=Bookmark)
async def get(
        bookmark_id: UUID,
        user_id: UUID = Depends(TokenCheck()),
        service: BaseBookmarkService = Depends(get_bookmarks_service)
):
    return handle_result(await service.get_one(item=BookmarkGet(
        bookmark_id=bookmark_id,
        user_id=user_id
    )))


@router.get('/bookmarks', response_model=Bookmarks)
async def get_list(
        user_id: UUID = Depends(TokenCheck()),
        service: BaseBookmarkService = Depends(get_bookmarks_service)
):
    return handle_result(await service.get_list(item=BookmarkGet(
        user_id=user_id,
    )))
