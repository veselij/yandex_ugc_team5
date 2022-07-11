import config
import pytest
from httpx import Headers

URL = f"http://{config.API_HOST}:{config.API_PORT}/api/v1/"
headers = Headers(
    {"Content-Type": "application/json", "Authorization": f"Bearer {config.TOKEN}"}
)


@pytest.mark.asyncio
async def test_create_bookmark():
    pass
