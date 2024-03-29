from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import Field

from models import Base
from utils.service_result import ServiceResult


class Bookmark(Base):
    bookmark_id: UUID = Field(default_factory=uuid4)
    movie_id: UUID
    user_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)


class BookmarkGet(Base):
    bookmark_id: Optional[UUID]
    movie_id: Optional[UUID]
    user_id: Optional[UUID]


class BookmarkCreate(Base):
    movie_id: UUID


class BookmarkDelete(Base):
    bookmark_id: UUID
    movie_id: UUID
    user_id: UUID


class Bookmarks(Base):
    items: List[Bookmark]
    count: int


class BaseBookmarkService(ABC):
    @abstractmethod
    async def create(self, item: Bookmark) -> ServiceResult:
        pass

    @abstractmethod
    async def delete(self, item: BookmarkDelete) -> ServiceResult:
        pass

    @abstractmethod
    async def get_one(self, item: BookmarkGet) -> ServiceResult:
        pass

    @abstractmethod
    async def get_list(self, item: BookmarkGet) -> ServiceResult:
        pass
