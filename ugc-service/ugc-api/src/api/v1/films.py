from fastapi.routing import APIRouter
from models import FilmWatchTimestamp

router = APIRouter()


@router.post(
    path="/",
    summary="Film timestamp API",
    description="Receives film watch timestamp",
)
async def recieve_film_timestamp(film_timestamp: FilmWatchTimestamp):
    print(film_timestamp)
    return
