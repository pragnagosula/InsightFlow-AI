from app.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository):
    collection_name = "conversations"

    async def find_by_workspace(self, workspace_id: str) -> list[dict]:
        return await self.find_many({"workspace_id": workspace_id}, sort=[("updated_at", -1)])


conversation_repo = ConversationRepository()
