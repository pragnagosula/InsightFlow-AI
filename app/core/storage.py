import shutil
from pathlib import Path

import aiofiles

from app.config import settings


def ensure_dirs() -> None:
    for d in (
        settings.UPLOADS_RAW_DIR,
        settings.UPLOADS_CLEANED_DIR,
        settings.FAISS_DIR,
        settings.CHARTS_DIR,
        settings.REPORTS_DIR,
    ):
        d.mkdir(parents=True, exist_ok=True)


async def save_upload(content: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(dest, "wb") as f:
        await f.write(content)


def raw_path(workspace_id: str, filename: str) -> Path:
    return settings.UPLOADS_RAW_DIR / workspace_id / filename


def cleaned_path(workspace_id: str, filename: str) -> Path:
    return settings.UPLOADS_CLEANED_DIR / workspace_id / filename


def faiss_index_path(document_id: str) -> Path:
    return settings.FAISS_DIR / f"{document_id}.index"


def faiss_meta_path(document_id: str) -> Path:
    return settings.FAISS_DIR / f"{document_id}.pkl"


def chart_path(chart_id: str) -> Path:
    return settings.CHARTS_DIR / f"{chart_id}.png"


def report_path(report_id: str) -> Path:
    return settings.REPORTS_DIR / f"{report_id}.pdf"


def delete_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def delete_workspace_files(workspace_id: str) -> None:
    for base in (settings.UPLOADS_RAW_DIR, settings.UPLOADS_CLEANED_DIR):
        ws_dir = base / workspace_id
        if ws_dir.exists():
            shutil.rmtree(ws_dir)
