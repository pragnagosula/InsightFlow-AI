"""
Preprocessing Agent wrapper — delegates to preprocessing_service.
Exists as an agent-layer boundary for consistency with the multi-agent design.
"""
from __future__ import annotations

from pathlib import Path

from app.services.preprocessing_service import run_pipeline


def preprocess(input_path: Path, output_path: Path) -> dict:
    return run_pipeline(input_path, output_path)
