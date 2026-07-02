from app.repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository):
    collection_name = "reports"

    async def find_by_workspace(self, workspace_id: str) -> list[dict]:
        return await self.find_many({"workspace_id": workspace_id}, sort=[("created_at", -1)])


class PreprocessingReportRepository(BaseRepository):
    collection_name = "preprocessing_reports"

    async def find_by_dataset(self, dataset_id: str) -> dict | None:
        docs = await self.find_many({"dataset_id": dataset_id}, limit=1)
        return docs[0] if docs else None


report_repo = ReportRepository()
preprocessing_report_repo = PreprocessingReportRepository()
