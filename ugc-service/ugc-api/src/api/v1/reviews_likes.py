from uuid import UUID

from fastapi import APIRouter, Depends

from auth import CustomHTTPAuthorizationCredentials, TokenCheck
from services.mongo.reviews_likes import get_review_likes_service
from services.reviews_likes import (
    BaseReviewLikesService,
    ReviewLike,
    ReviewLikeCreate,
    ReviewLikeDelete,
    ReviewLikeGet,
    ReviewLikes,
)
from utils.service_result import handle_result

router = APIRouter()


@router.post("/reviews/likes", response_model=ReviewLike)
async def create(
    like: ReviewLikeCreate,
    user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck()),
    service: BaseReviewLikesService = Depends(get_review_likes_service),
):
    return handle_result(
        await service.create(
            item=ReviewLike(
                review_id=like.review_id,
                user_id=UUID(user_credentials.user_id),
                value=like.value,
            )
        )
    )


@router.delete("/reviews/{review_id}/likes/{like_id}")
async def delete(
    like_id: UUID,
    review_id: UUID,
    user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck()),
    service: BaseReviewLikesService = Depends(get_review_likes_service),
):
    return handle_result(
        await service.delete(
            item=ReviewLikeDelete(
                review_id=review_id,
                like_id=like_id,
                user_id=UUID(user_credentials.user_id),
            )
        )
    )


@router.get("/reviews/{review_id}/likes", response_model=ReviewLikes)
async def get_list(
    review_id: UUID, service: BaseReviewLikesService = Depends(get_review_likes_service)
):
    return handle_result(
        await service.get_list(item=ReviewLikeGet(review_id=review_id))
    )


@router.get("/user/reviews/likes", response_model=ReviewLikes)
async def get_list_by_user(
    user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck()),
    service: BaseReviewLikesService = Depends(get_review_likes_service),
):
    return handle_result(
        await service.get_list(item=ReviewLikeGet(user_id=user_credentials.user_id))
    )
