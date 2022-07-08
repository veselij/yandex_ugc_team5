from uuid import UUID

from fastapi import APIRouter, Depends

from auth import TokenCheck
from services.mongo.reviews import get_reviews_service
from services.reviews import Review, Reviews, ReviewCreate, BaseReviewsService, ReviewGetPublic, ReviewGetAuth, \
    ReviewDelete
from utils.service_result import handle_result

router = APIRouter()


@router.post("/reviews", response_model=Review)
async def create(
        item: ReviewCreate,
        user_id: UUID = Depends(TokenCheck()),
        service: BaseReviewsService = Depends(get_reviews_service)
):
    review = Review(
        user_id=user_id,
        movie_id=item.movie_id,
        text=item.text
    )
    result = await service.create(review)
    return handle_result(result)


@router.delete("/reviews/{review_id}")
async def delete(
        review_id: UUID,
        user_id: UUID = Depends(TokenCheck()),
        service: BaseReviewsService = Depends(get_reviews_service)
):
    result = await service.delete(ReviewDelete(
        review_id=review_id,
        user_id=user_id
    ))
    return handle_result(result)


@router.get("/reviews/{review_id}", response_model=Review)
async def get(review_id: UUID, service: BaseReviewsService = Depends(get_reviews_service)):
    result = await service.get_one(ReviewGetPublic(
        review_id=review_id
    ))
    return handle_result(result)


@router.get("/reviews/movies/{movie_id}", response_model=Reviews)
async def get_list(
        movie_id: UUID,
        service: BaseReviewsService = Depends(get_reviews_service)
):
    result = await service.get_list(ReviewGetPublic(
        movie_id=movie_id
    ))
    return handle_result(result)


@router.get('/user/reviews', response_model=Reviews)
async def get_list_with_auth(
        user_id: UUID = Depends(TokenCheck()),
        service: BaseReviewsService = Depends(get_reviews_service)
):
    return handle_result(await service.get_list(item=ReviewGetAuth(
        user_id=user_id,
    )))
