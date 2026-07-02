from app.repositories.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository):
    collection_name = "workspaces"

    async def find_all(self) -> list[dict]:
        return await self.find_many({}, sort=[("updated_at", -1)])

    async def find_by_id(self, id_str: str) -> dict | None:
        return await super().find_by_id(id_str)


workspace_repo = WorkspaceRepository()
