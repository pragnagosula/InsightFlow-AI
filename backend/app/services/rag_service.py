"""
RAG service: text extraction, chunking, embedding, FAISS indexing, retrieval.
"""
from __future__ import annotations

from pathlib import Path

from app.config import settings
from app.core.embeddings import embed_texts, embed_query
from app.core.vector_store import VectorStore


# ---------------------------------------------------------------------------
# Build index (called once after document upload)
# ---------------------------------------------------------------------------

def build_index_for_document(document_id: str, path: Path, suffix: str) -> int:
    text = _extract_text(path, suffix)
    chunks = _chunk_text(text)
    if not chunks:
        return 0
    embeddings = embed_texts(chunks)
    vs = VectorStore(document_id)
    vs.build(chunks, embeddings)
    vs.save()
    return len(chunks)


# ---------------------------------------------------------------------------
# Retrieve (called per query)
# ---------------------------------------------------------------------------

def retrieve(document_id: str, query: str, top_k: int | None = None) -> list[str]:
    k = top_k or settings.RAG_TOP_K
    q_vec = embed_query(query)
    vs = VectorStore(document_id)
    return vs.search(q_vec, top_k=k)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def _extract_text(path: Path, suffix: str) -> str:
    suffix = suffix.lower().lstrip(".")
    if suffix == "pdf":
        return _extract_pdf(path)
    if suffix == "docx":
        return _extract_docx(path)
    if suffix in ("txt", "md"):
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def _extract_pdf(path: Path) -> str:
    import fitz  # pymupdf
    doc = fitz.open(str(path))
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages)


def _extract_docx(path: Path) -> str:
    from docx import Document
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def _chunk_text(text: str) -> list[str]:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return [c for c in splitter.split_text(text) if c.strip()]
