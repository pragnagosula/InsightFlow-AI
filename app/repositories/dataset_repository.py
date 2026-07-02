from app.repositories.base_repository import BaseRepository


class DatasetRepository(BaseRepository):
    collection_name = "datasets"

    async def find_by_workspace(self, workspace_id: str) -> list[dict]:
        return await self.find_many({"workspace_id": workspace_id}, sort=[("created_at", -1)])

    async def update_status(self, dataset_id: str, status: str, extra: dict | None = None) -> bool:
        fields = {"preprocessing_status": status}
        if extra:
            fields.update(extra)
        return await self.set_fields(dataset_id, fields)


dataset_repo = DatasetRepository()
