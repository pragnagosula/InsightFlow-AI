from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # App
    APP_NAME: str = "InsightFlow AI"
    DEBUG: bool = False

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "insightflow"

    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # Storage paths (resolved at runtime from BASE_DIR)
    STORAGE_DIR: Path = BASE_DIR / "storage"
    UPLOADS_RAW_DIR: Path = BASE_DIR / "storage" / "uploads" / "raw"
    UPLOADS_CLEANED_DIR: Path = BASE_DIR / "storage" / "uploads" / "cleaned"
    FAISS_DIR: Path = BASE_DIR / "storage" / "faiss_indexes"
    CHARTS_DIR: Path = BASE_DIR / "storage" / "charts"
    REPORTS_DIR: Path = BASE_DIR / "storage" / "reports"

    # RAG / Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    RAG_TOP_K: int = 5

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
