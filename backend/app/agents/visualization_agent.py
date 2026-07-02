"""
Visualization Agent — decides chart type and produces Plotly JSON + PNG.
Only called when Planner sets needs_chart=True.
"""
from __future__ import annotations

import io
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from app.config import settings


def generate_chart(
    dataset_paths: list[str],
    question: str,
    chart_hint: str,
) -> dict | None:
    """
    Returns {"chart_type", "title", "plotly_json", "image_path"} or None.
    """
    if not dataset_paths:
        return None

    df = _load_first(dataset_paths)
    if df is None or df.empty:
        return None

    chart_type = chart_hint or _infer_chart_type(df, question)
    fig = _build_figure(df, chart_type, question)
    if fig is None:
        return None

    title = _make_title(question, chart_type)
    fig.update_layout(title=title, template="plotly_white")
    # to_json() serializes numpy arrays/scalars to plain Python types (BSON can't encode numpy types)
    plotly_json = json.loads(pio.to_json(fig))

    image_path = _save_image(fig)

    return {
        "chart_type": chart_type,
        "title": title,
        "plotly_json": plotly_json,
        "image_path": str(image_path) if image_path else "",
    }


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------

def _load_first(paths: list[str]) -> pd.DataFrame | None:
    for p in paths:
        path = Path(p)
        if path.exists():
            return pd.read_csv(path)
    return None


def _infer_chart_type(df: pd.DataFrame, question: str) -> str:
    q = question.lower()
    if any(w in q for w in ("trend", "over time", "monthly", "yearly", "daily")):
        return "line"
    if any(w in q for w in ("top", "most", "least", "rank", "compare")):
        return "bar"
    if any(w in q for w in ("distribution", "spread", "histogram")):
        return "histogram"
    if any(w in q for w in ("correlation", "relationship", "scatter")):
        return "scatter"
    if any(w in q for w in ("share", "proportion", "percent", "pie")):
        return "pie"
    return "bar"


def _build_figure(df: pd.DataFrame, chart_type: str, question: str) -> go.Figure | None:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]

    if not numeric_cols:
        return None

    y_col = numeric_cols[0]
    x_col = date_cols[0] if date_cols else (cat_cols[0] if cat_cols else None)

    try:
        if chart_type == "line" and x_col:
            return px.line(df.head(200), x=x_col, y=y_col)
        if chart_type == "bar" and x_col:
            agg = df.groupby(x_col)[y_col].sum().reset_index().head(20)
            return px.bar(agg, x=x_col, y=y_col)
        if chart_type == "histogram":
            return px.histogram(df.head(500), x=y_col, nbins=30)
        if chart_type == "scatter" and len(numeric_cols) >= 2:
            return px.scatter(df.head(500), x=numeric_cols[0], y=numeric_cols[1])
        if chart_type == "pie" and x_col:
            agg = df.groupby(x_col)[y_col].sum().reset_index().head(10)
            return px.pie(agg, names=x_col, values=y_col)
        if chart_type == "heatmap" and len(numeric_cols) >= 2:
            corr = df[numeric_cols[:10]].corr().round(2)
            return px.imshow(corr, text_auto=True, aspect="auto")
        # Fallback
        if x_col:
            return px.bar(df.head(30), x=x_col, y=y_col)
    except Exception:
        return None
    return None


def _save_image(fig: go.Figure) -> Path | None:
    import uuid
    chart_id = str(uuid.uuid4())
    path = settings.CHARTS_DIR / f"{chart_id}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.write_image(str(path), format="png", width=900, height=500, scale=2)
        return path
    except Exception:
        return None


def _make_title(question: str, chart_type: str) -> str:
    short = question[:60].rstrip() + ("…" if len(question) > 60 else "")
    return f"{chart_type.title()} Chart — {short}"
