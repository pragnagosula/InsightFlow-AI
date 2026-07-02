from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

_client: AsyncIOMotorClient | None = None


async def connect_db():
    global _client

    print("Mongo URL:", settings.MONGODB_URL)
    print("DB:", settings.MONGODB_DB_NAME)

    _client = AsyncIOMotorClient(settings.MONGODB_URL)
    await _client.admin.command("ping")


async def close_db() -> None:
    global _client
    if _client:
        _client.close()
        _client = None


def get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Database client not initialized. Call connect_db() first.")
    return _client[settings.MONGODB_DB_NAME]
