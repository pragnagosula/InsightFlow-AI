import pickle
from pathlib import Path

import faiss
import numpy as np

from app.core.storage import faiss_index_path, faiss_meta_path


class VectorStore:
    """Per-document FAISS index with chunk metadata."""

    def __init__(self, document_id: str):
        self.document_id = document_id
        self._index: faiss.IndexFlatL2 | None = None
        self._chunks: list[str] = []

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, chunks: list[str], embeddings: list[list[float]]) -> None:
        vectors = np.array(embeddings, dtype="float32")
        dim = vectors.shape[1]
        self._index = faiss.IndexFlatL2(dim)
        self._index.add(vectors)
        self._chunks = chunks

    # ------------------------------------------------------------------
    # Persist
    # ------------------------------------------------------------------

    def save(self) -> None:
        idx_path = faiss_index_path(self.document_id)
        meta_path = faiss_meta_path(self.document_id)
        idx_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(idx_path))
        with open(meta_path, "wb") as f:
            pickle.dump(self._chunks, f)

    def load(self) -> None:
        idx_path = faiss_index_path(self.document_id)
        meta_path = faiss_meta_path(self.document_id)
        if not idx_path.exists():
            raise FileNotFoundError(f"FAISS index not found for document {self.document_id}")
        self._index = faiss.read_index(str(idx_path))
        with open(meta_path, "rb") as f:
            self._chunks = pickle.load(f)

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[str]:
        if self._index is None:
            self.load()
        vector = np.array([query_embedding], dtype="float32")
        k = min(top_k, len(self._chunks))
        _, indices = self._index.search(vector, k)
        return [self._chunks[i] for i in indices[0] if i < len(self._chunks)]

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    @staticmethod
    def delete(document_id: str) -> None:
        for p in (faiss_index_path(document_id), faiss_meta_path(document_id)):
            if p.exists():
                p.unlink()
