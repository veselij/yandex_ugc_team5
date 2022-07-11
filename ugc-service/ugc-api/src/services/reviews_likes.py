from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import Field

from models import Base
from utils.service_result import ServiceResult


class ReviewLike(Base):
    like_id: UUID = Field(default_factory=uuid4)
    review_id: UUID
    user_id: UUID
    value: int
    created_at: datetime = Field(default_factory=datetime.now)


class ReviewLikeGet(Base):
    like_id: Optional[UUID]
    review_id: Optional[UUID]
    user_id: Optional[UUID]


class ReviewLikeCreate(Base):
    review_id: UUID
    value: int


class ReviewLikeDelete(Base):
    review_id: UUID
    like_id: UUID
    user_id: UUID


class ReviewLikes(Base):
    items: List[ReviewLike]
    count: int


class BaseReviewLikesService(ABC):
    @abstractmethod
    async def create(self, item: ReviewLike) -> ServiceResult:
        pass

    @abstractmethod
    async def delete(self, item: ReviewLikeDelete) -> ServiceResult:
        pass

    @abstractmethod
    async def get_one(self, item: ReviewLikeGet) -> ServiceResult:
        pass

    @abstractmethod
    async def get_list(self, item: ReviewLikeGet) -> ServiceResult:
        pass
