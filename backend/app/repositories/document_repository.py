from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):
    collection_name = "documents"

    async def find_by_workspace(self, workspace_id: str) -> list[dict]:
        return await self.find_many({"workspace_id": workspace_id}, sort=[("created_at", -1)])

    async def update_status(self, doc_id: str, status: str, extra: dict | None = None) -> bool:
        fields = {"embedding_status": status}
        if extra:
            fields.update(extra)
        return await self.set_fields(doc_id, fields)


document_repo = DocumentRepository()
