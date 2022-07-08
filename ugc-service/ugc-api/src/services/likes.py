from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from utils.service_result import ServiceResult


class Like(BaseModel):
    like_id: UUID = Field(default_factory=uuid4)
    movie_id: UUID
    user_id: UUID
    value: int
    created_at: datetime = Field(default_factory=datetime.now)


class LikeGet(BaseModel):
    like_id: Optional[UUID]
    movie_id: Optional[UUID]
    rating_id: Optional[UUID]
    user_id: Optional[UUID]


class LikeCreate(BaseModel):
    movie_id: UUID
    value: int


class LikeDelete(BaseModel):
    like_id: UUID
    user_id: UUID


class Likes(BaseModel):
    items: List[Like]
    count: int


class BaseLikesService(ABC):
    @abstractmethod
    async def create(self, item: Like) -> ServiceResult:
        pass

    @abstractmethod
    async def delete(self, item: LikeDelete) -> ServiceResult:
        pass

    @abstractmethod
    async def get_one(self, item: LikeGet) -> ServiceResult:
        pass

    @abstractmethod
    async def get_list(self, item: LikeGet) -> ServiceResult:
        pass
