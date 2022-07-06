from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmWatchTimestamp(BaseModel):
    user_id: Optional[str]
    film_id: UUID
    film_timestamp: int


class Like(BaseModel):
    rating: int

