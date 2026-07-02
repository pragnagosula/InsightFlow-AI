from app.repositories.base_repository import BaseRepository


class ChartRepository(BaseRepository):
    collection_name = "charts"

    async def find_by_workspace(self, workspace_id: str) -> list[dict]:
        return await self.find_many({"workspace_id": workspace_id}, sort=[("created_at", -1)])

    async def find_by_message(self, message_id: str) -> list[dict]:
        return await self.find_many({"message_id": message_id})


chart_repo = ChartRepository()
