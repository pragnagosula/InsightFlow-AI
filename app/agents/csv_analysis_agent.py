"""
CSV Analysis Agent — runs statistical analysis on cleaned datasets.
Returns a structured summary dict, never raw data.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def analyse(dataset_paths: list[str], question: str, query_type: str) -> dict:
    """
    Loads cleaned CSVs and produces an analysis summary.
    Returns a dict consumed by the Knowledge Fusion Agent.
    """
    if not dataset_paths:
        return {}

    frames = {Path(p).stem: _load(p) for p in dataset_paths if Path(p).exists()}
    if not frames:
        return {}

    summary = {
        "datasets_analysed": list(frames.keys()),
        "statistics": {},
        "insights": [],
    }

    for name, df in frames.items():
        summary["statistics"][name] = _describe(df)

    if query_type in ("trend", "comparison", "hybrid"):
        for name, df in frames.items():
            summary["insights"] += _trend_insights(df, name)

    if query_type == "correlation":
        for name, df in frames.items():
            summary["correlation"] = _correlation(df)

    if len(frames) > 1:
        summary["multi_dataset_note"] = (
            "Multiple datasets loaded. Cross-dataset analysis requires matching columns."
        )

    return summary


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------

def _load(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def _describe(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include=[np.number])
    desc = numeric.describe().round(4).to_dict() if not numeric.empty else {}
    return {
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing_values": df.isna().sum().to_dict(),
        "numeric_stats": desc,
        "sample_values": {
            col: df[col].dropna().head(3).tolist()
            for col in df.columns[:10]
        },
    }


def _trend_insights(df: pd.DataFrame, name: str) -> list[str]:
    insights = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols[:3]:
        series = df[col].dropna()
        if len(series) < 2:
            continue
        delta = series.iloc[-1] - series.iloc[0]
        direction = "increased" if delta > 0 else "decreased"
        pct = abs(delta / series.iloc[0] * 100) if series.iloc[0] != 0 else 0
        insights.append(
            f"[{name}] {col}: {direction} by {pct:.1f}% from first to last record."
        )
    return insights


def _correlation(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return {}
    corr = numeric.corr().round(4)
    pairs = []
    cols = list(corr.columns)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append({
                "col_a": cols[i],
                "col_b": cols[j],
                "correlation": corr.iloc[i, j],
            })
    pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return {"top_correlations": pairs[:10]}
