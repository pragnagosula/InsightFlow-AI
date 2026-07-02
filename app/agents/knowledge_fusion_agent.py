"""
Knowledge Fusion Agent — assembles all analysis results into a
single structured context dict that gets passed to the Insight Agent.
The raw data (DataFrames, chunks) is never sent directly to Gemini.
"""
from __future__ import annotations

import json


def fuse(
    question: str,
    history: list[dict],
    plan: dict,
    csv_summary: dict,
    rag_result: dict,
    chart_info: dict | None,
) -> str:
    """
    Returns a single formatted string context for the Insight Agent.
    """
    parts: list[str] = []

    parts.append(f"USER QUESTION:\n{question}\n")

    if history:
        recent = history[-4:]
        h_text = "\n".join(
            f"{m['role'].upper()}: {m['content'][:400]}" for m in recent
        )
        parts.append(f"RECENT CONVERSATION CONTEXT:\n{h_text}\n")

    if csv_summary:
        parts.append("CSV ANALYSIS RESULTS:")
        parts.append(f"Datasets analysed: {', '.join(csv_summary.get('datasets_analysed', []))}")
        stats = csv_summary.get("statistics", {})
        for name, stat in stats.items():
            shape = stat.get("shape", {})
            parts.append(f"\n[{name}] — {shape.get('rows')} rows × {shape.get('columns')} columns")
            num_stats = stat.get("numeric_stats", {})
            if num_stats:
                parts.append("  Key statistics:")
                for col, vals in list(num_stats.items())[:5]:
                    mean = vals.get("mean", "N/A")
                    parts.append(f"    {col}: mean={mean}, min={vals.get('min','N/A')}, max={vals.get('max','N/A')}")
        for insight in csv_summary.get("insights", []):
            parts.append(f"  Trend insight: {insight}")
        if "correlation" in csv_summary:
            pairs = csv_summary["correlation"].get("top_correlations", [])[:5]
            for p in pairs:
                parts.append(f"  Correlation: {p['col_a']} ↔ {p['col_b']} = {p['correlation']:.3f}")

    if rag_result and rag_result.get("context_text"):
        parts.append("\nDOCUMENT CONTEXT (retrieved via semantic search):")
        parts.append(rag_result["context_text"][:6000])
        citations = rag_result.get("citations", [])
        if citations:
            parts.append(f"\nSources: {', '.join(citations)}")

    if chart_info:
        parts.append(
            f"\nVISUALIZATION: A {chart_info['chart_type']} chart titled "
            f'"{chart_info["title"]}" has been generated and will be shown to the user.'
        )

    return "\n".join(parts)
