"""
RAG Agent — retrieves relevant document chunks and formats them with citations.
"""
from __future__ import annotations

from app.config import settings
from app.services.rag_service import retrieve


def retrieve_context(
    document_ids: list[str],
    document_filenames: dict[str, str],
    question: str,
    top_k: int | None = None,
) -> dict:
    """
    Returns {"chunks": [...], "citations": [...], "context_text": "..."}.
    document_filenames maps document_id -> filename for citation.
    """
    if not document_ids:
        return {"chunks": [], "citations": [], "context_text": ""}

    k = top_k or settings.RAG_TOP_K
    all_chunks: list[str] = []
    citations: list[str] = []

    snippets_by_source: dict[str, list[str]] = {}

    for doc_id in document_ids:
        filename = document_filenames.get(doc_id, doc_id)
        try:
            chunks = retrieve(doc_id, question, top_k=k)
            if not chunks:
                continue
            per_doc: list[str] = []
            for i, chunk in enumerate(chunks, 1):
                labelled = f"[{filename} — chunk {i}]\n{chunk}"
                all_chunks.append(labelled)
                per_doc.append(chunk)
            citations.append(filename)
            snippets_by_source[filename] = per_doc
        except FileNotFoundError:
            pass

    context_text = "\n\n---\n\n".join(all_chunks)
    return {
        "chunks": all_chunks,
        "citations": citations,
        "context_text": context_text,
        "snippets_by_source": snippets_by_source,
    }
