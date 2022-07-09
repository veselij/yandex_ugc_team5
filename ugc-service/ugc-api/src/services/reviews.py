from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from utils.service_result import ServiceResult


class Review(BaseModel):
    review_id: UUID = Field(default_factory=uuid4)
    movie_id: UUID
    user_id: UUID
    text: str
    created_at: datetime = Field(default_factory=datetime.now)


class ReviewCreate(BaseModel):
    movie_id: UUID
    text: str


class ReviewDelete(BaseModel):
    review_id: UUID
    user_id: UUID


class ReviewGetPublic(BaseModel):
    review_id: Optional[UUID]
    movie_id: Optional[UUID]


class ReviewGetAuth(BaseModel):
    review_id: Optional[UUID]
    movie_id: Optional[UUID]
    user_id: UUID


class Reviews(BaseModel):
    items: List[Review]


class BaseReviewsService(ABC):
    @abstractmethod
    async def create(self, item: Review) -> ServiceResult:
        pass

    @abstractmethod
    async def delete(self, item: ReviewDelete) -> ServiceResult:
        pass

    @abstractmethod
    async def get_one(self, item: ReviewGetPublic) -> ServiceResult:
        pass

    @abstractmethod
    async def get_list(self, item: ReviewGetPublic) -> ServiceResult:
        pass
