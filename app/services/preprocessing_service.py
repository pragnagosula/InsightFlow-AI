"""
CSV/XLSX preprocessing pipeline.
Original file is NEVER modified. A cleaned copy is produced.
"""
from __future__ import annotations

import re
from pathlib import Path

import chardet
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_pipeline(input_path: Path, output_path: Path) -> dict:
    """
    Run the full preprocessing pipeline.
    Returns a report dict describing every transformation applied.
    """
    log: list[str] = []
    report: dict = {}

    # 1. Detect encoding & load
    encoding = _detect_encoding(input_path)
    log.append(f"Detected encoding: {encoding}")

    df = _load(input_path, encoding)
    original_rows = len(df)
    original_cols = list(df.columns)
    report["original_rows"] = original_rows
    report["original_columns"] = original_cols
    log.append(f"Loaded {original_rows} rows × {len(original_cols)} columns")

    # 2. Normalize column names
    df, renamed = _normalize_columns(df)
    if renamed:
        log.append(f"Renamed columns: {renamed}")

    # 3. Remove constant columns
    df, removed_cols = _remove_constant_columns(df)
    report["removed_columns"] = removed_cols
    if removed_cols:
        log.append(f"Removed constant columns: {removed_cols}")

    # 4. Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    removed_dupes = before - len(df)
    report["removed_duplicates"] = removed_dupes
    log.append(f"Removed {removed_dupes} duplicate rows")

    # 5. Trim string whitespace
    df = _trim_whitespace(df)
    log.append("Trimmed whitespace in all string columns")

    # 6. Detect & convert dtypes
    df, type_conversions = _convert_dtypes(df)
    report["type_conversions"] = type_conversions
    if type_conversions:
        log.append(f"Type conversions: {type_conversions}")

    # 7. Normalize date columns
    df, date_cols = _normalize_dates(df)
    if date_cols:
        log.append(f"Normalized date columns: {date_cols}")

    # 8. Standardize categorical values (strip & title-case low-cardinality strings)
    df = _standardize_categoricals(df)
    log.append("Standardized categorical string values")

    # 9. Handle missing values
    df, null_fills = _handle_missing(df)
    report["null_fills"] = null_fills
    log.append(f"Filled nulls: {null_fills}")

    # 10. Handle outliers (IQR)
    df, outliers_handled = _handle_outliers(df)
    report["outliers_handled"] = outliers_handled
    log.append(f"Capped {outliers_handled} outlier values using IQR")

    # 11. Save cleaned file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    cleaned_rows = len(df)
    report["cleaned_rows"] = cleaned_rows
    report["detailed_log"] = log
    report["quality_score"] = _compute_quality_score(original_rows, cleaned_rows, df)
    report["columns"] = list(df.columns)
    report["row_count"] = cleaned_rows

    return report


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

def _detect_encoding(path: Path) -> str:
    with open(path, "rb") as f:
        raw = f.read(100_000)
    result = chardet.detect(raw)
    return result.get("encoding") or "utf-8"


def _is_real_excel(path: Path) -> bool:
    """Check the actual file signature rather than trusting the extension.

    Files named .xls are sometimes plain CSV/HTML exported by other tools,
    which makes pandas' Excel engines fail even though the extension says
    otherwise.
    """
    with open(path, "rb") as f:
        header = f.read(8)
    return header.startswith(b"PK\x03\x04") or header.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")


def _load(path: Path, encoding: str) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls") and _is_real_excel(path):
        return pd.read_excel(path)
    # Try comma first, then fallback to auto-detection
    try:
        return pd.read_csv(path, encoding=encoding, sep=",")
    except Exception:
        return pd.read_csv(path, encoding=encoding, sep=None, engine="python")


def _normalize_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    renamed = {}
    new_cols = []
    for col in df.columns:
        clean = re.sub(r"\s+", "_", col.strip().lower())
        clean = re.sub(r"[^\w]", "_", clean)
        clean = re.sub(r"_+", "_", clean).strip("_")
        if clean != col:
            renamed[col] = clean
        new_cols.append(clean)
    df.columns = new_cols
    return df, renamed


def _remove_constant_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    removed = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]
    return df.drop(columns=removed), removed


def _trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda s: s.str.strip())
    return df


def _convert_dtypes(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    conversions = []
    for col in df.columns:
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > 0.8 * df[col].notna().sum():
                conversions.append({"column": col, "from": "object", "to": "numeric"})
                df[col] = converted
    return df, conversions


def _normalize_dates(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    date_cols = []
    for col in df.columns:
        if "date" in col or "time" in col or "dt" in col:
            converted = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)
            if converted.notna().sum() > 0.5 * len(df):
                df[col] = converted
                date_cols.append(col)
    return df, date_cols


def _standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include="object").columns:
        if df[col].nunique() < 50:
            df[col] = df[col].str.title()
    return df


def _handle_missing(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    fills: dict = {}
    for col in df.columns:
        null_count = df[col].isna().sum()
        if null_count == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            median = df[col].median()
            df[col] = df[col].fillna(median)
            fills[col] = f"median({median:.4g})"
        else:
            mode_vals = df[col].mode()
            if len(mode_vals) > 0:
                df[col] = df[col].fillna(mode_vals[0])
                fills[col] = f"mode({mode_vals[0]})"
    return df, fills


def _handle_outliers(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    total_capped = 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        total_capped += int(mask.sum())
        df[col] = df[col].clip(lower=lower, upper=upper)
    return df, total_capped


def _compute_quality_score(original_rows: int, cleaned_rows: int, df: pd.DataFrame) -> float:
    if original_rows == 0:
        return 0.0
    completeness = 1 - df.isna().sum().sum() / max(df.size, 1)
    retention = cleaned_rows / original_rows
    return round(min(1.0, (completeness * 0.6 + retention * 0.4)), 4)
