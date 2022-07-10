from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import Field

from models import Base
from utils.service_result import ServiceResult


class Review(Base):
    review_id: UUID = Field(default_factory=uuid4)
    movie_id: UUID
    user_id: UUID
    text: str
    created_at: datetime = Field(default_factory=datetime.now)


class ReviewCreate(Base):
    movie_id: UUID
    text: str


class ReviewDelete(Base):
    review_id: UUID
    user_id: UUID


class ReviewGet(Base):
    review_id: Optional[UUID]
    movie_id: Optional[UUID]
    user_id: UUID


class Reviews(Base):
    items: List[Review]


class BaseReviewsService(ABC):
    @abstractmethod
    async def create(self, item: Review) -> ServiceResult:
        pass

    @abstractmethod
    async def delete(self, item: ReviewDelete) -> ServiceResult:
        pass

    @abstractmethod
    async def get_one(self, item: ReviewGet) -> ServiceResult:
        pass

    @abstractmethod
    async def get_list(self, item: ReviewGet) -> ServiceResult:
        pass
