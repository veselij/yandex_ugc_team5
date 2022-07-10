from typing import Optional

import motor.motor_asyncio

mongo_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None


async def get_mongo() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    if mongo_client:
        return mongo_client.ugc
