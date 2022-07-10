from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from auth import CustomHTTPAuthorizationCredentials, TokenCheck
from services.likes import (
    BaseLikesService,
    Like,
    LikeCreate,
    LikeDelete,
    LikeGet,
    Likes,
)
from services.mongo.likes import get_likes_service
from utils.service_result import handle_result

router = APIRouter()


@router.post('/movies/likes', response_model=Like)
async def create(
        like: LikeCreate,
        user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck()),
        service: BaseLikesService = Depends(get_likes_service)
):
    return handle_result(await service.create(item=Like(
        movie_id=like.movie_id,
        user_id=user_credentials.user_id,
        value=like.value
    )))


@router.delete('/movies/likes/{like_id}')
async def delete(
        like_id: UUID,
        user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck()),
        service: BaseLikesService = Depends(get_likes_service)
):
    return handle_result(await service.delete(item=LikeDelete(
        like_id=like_id,
        user_id=user_credentials.user_id,
    )))


@router.get('/movies/likes/{like_id}', response_model=Like)
async def get(
        like_id: UUID,
        service: BaseLikesService = Depends(get_likes_service)
):
    return handle_result(await service.get_one(item=LikeGet(
        like_id=like_id,
    )))


@router.get('/movies/{movie_id}/likes', response_model=Likes)
async def get_list(
        movie_id: Optional[UUID],
        service: BaseLikesService = Depends(get_likes_service)
):
    return handle_result(await service.get_list(item=LikeGet(
        movie_id=movie_id,
    )))


@router.get('/user/movies/likes', response_model=Likes)
async def get_list_with_auth(
        movie_id: Optional[UUID],
        user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck()),
        service: BaseLikesService = Depends(get_likes_service)
):
    return handle_result(await service.get_list(item=LikeGet(
        user_id=user_credentials.user_id,
        movie_id=movie_id,
    )))
