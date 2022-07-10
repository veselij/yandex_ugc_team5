from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from auth import CustomHTTPAuthorizationCredentials, TokenCheck
from kafka_service import send_to_kafka
from models import FilmWatchTimestamp

router = APIRouter()


@router.post(
    path="/",
    summary="Film timestamp API",
    description="Receives film watch timestamp",
)
async def recieve_film_timestamp(
    film_timestamp: FilmWatchTimestamp, user_credentials: CustomHTTPAuthorizationCredentials = Depends(TokenCheck())
):
    film_timestamp.user_id = user_credentials.user_id
    await send_to_kafka(film_timestamp)
    return
