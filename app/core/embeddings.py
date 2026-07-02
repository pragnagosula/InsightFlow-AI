from sentence_transformers import SentenceTransformer
from app.config import settings

_model: SentenceTransformer | None = None


def load_embedding_model() -> None:
    global _model
    _model = SentenceTransformer(settings.EMBEDDING_MODEL)


def get_embedding_model() -> SentenceTransformer:
    if _model is None:
        raise RuntimeError("Embedding model not loaded. Call load_embedding_model() first.")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return model.encode(texts, show_progress_bar=False).tolist()


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]
