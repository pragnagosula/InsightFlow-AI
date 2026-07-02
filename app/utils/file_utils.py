from pathlib import Path

DATASET_EXTENSIONS = {".csv", ".xlsx", ".xls"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


def file_kind(filename: str) -> str:
    """Returns 'dataset', 'document', or raises ValueError."""
    suffix = Path(filename).suffix.lower()
    if suffix in DATASET_EXTENSIONS:
        return "dataset"
    if suffix in DOCUMENT_EXTENSIONS:
        return "document"
    raise ValueError(f"Unsupported file type: {suffix}")


def safe_filename(filename: str) -> str:
    """Remove path components and dangerous characters."""
    name = Path(filename).name
    return "".join(c for c in name if c.isalnum() or c in "._- ")


def file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024) if path.exists() else 0.0
