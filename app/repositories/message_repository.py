from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository):
    collection_name = "messages"

    async def find_by_conversation(self, conversation_id: str) -> list[dict]:
        return await self.find_many({"conversation_id": conversation_id}, sort=[("created_at", 1)])

    async def get_recent(self, conversation_id: str, n: int = 10) -> list[dict]:
        docs = await self.find_many(
            {"conversation_id": conversation_id},
            sort=[("created_at", -1)],
            limit=n,
        )
        return list(reversed(docs))


message_repo = MessageRepository()
