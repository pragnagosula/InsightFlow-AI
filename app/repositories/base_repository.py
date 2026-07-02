from datetime import datetime
from typing import Any, TypeVar, Generic, Type

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.core.database import get_db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    collection_name: str
    model_class: Type[T]

    def _col(self) -> AsyncIOMotorCollection:
        return get_db()[self.collection_name]

    @staticmethod
    def _to_id(id_str: str) -> ObjectId:
        return ObjectId(id_str)

    @staticmethod
    def _serialize(doc: dict) -> dict:
        """Convert ObjectId fields to str for Pydantic."""
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def insert(self, data: dict) -> str:
        data.pop("_id", None)
        result = await self._col().insert_one(data)
        return str(result.inserted_id)

    async def find_by_id(self, id_str: str) -> dict | None:
        doc = await self._col().find_one({"_id": self._to_id(id_str)})
        return self._serialize(doc) if doc else None

    async def find_many(self, filter_: dict, sort: list | None = None, limit: int = 0) -> list[dict]:
        cursor = self._col().find(filter_)
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        docs = await cursor.to_list(length=None)
        return [self._serialize(d) for d in docs]

    async def update_by_id(self, id_str: str, update: dict) -> bool:
        update.setdefault("$set", {})["updated_at"] = datetime.utcnow()
        result = await self._col().update_one(
            {"_id": self._to_id(id_str)}, update
        )
        return result.modified_count > 0

    async def set_fields(self, id_str: str, fields: dict) -> bool:
        fields["updated_at"] = datetime.utcnow()
        result = await self._col().update_one(
            {"_id": self._to_id(id_str)}, {"$set": fields}
        )
        return result.modified_count > 0

    async def delete_by_id(self, id_str: str) -> bool:
        result = await self._col().delete_one({"_id": self._to_id(id_str)})
        return result.deleted_count > 0

    async def count(self, filter_: dict) -> int:
        return await self._col().count_documents(filter_)

    async def delete_many(self, filter_: dict) -> int:
        result = await self._col().delete_many(filter_)
        return result.deleted_count
