import asyncio

import config
import httpx
import pytest
from clickhouse_driver import Client
from fake_data import films_data
from httpx import Headers

URL = f"http://{config.API_HOST}:{config.API_PORT}/api/v1/"
headers = Headers(
    {"Content-Type": "application/json", "Authorization": f"Bearer {config.TOKEN}"}
)


@pytest.mark.asyncio
async def test_film_timestamp_insert():
    client_clickhouse = Client(host=config.CLICKHOUSE_HOST1, port=config.CLICKHOUSE_PORT)

    for film in films_data:
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, headers=headers, json=film)
            assert response.status_code == httpx.codes.OK

    await asyncio.sleep(30)
    result = client_clickhouse.execute("SELECT * FROM film_watch_status")
    assert len(result) == len(films_data)


@pytest.mark.asyncio
async def test_film_timestamp_insert():
    client_clickhouse = Client(host=config.CLICKHOUSE_HOST1, port=config.CLICKHOUSE_PORT)

    for film in films_data:
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, headers=headers, json=film)
            assert response.status_code == httpx.codes.OK

    await asyncio.sleep(30)
    result = client_clickhouse.execute("SELECT * FROM film_watch_status")
    assert len(result) == len(films_data)
