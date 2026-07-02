"""
Planner Agent — determines which files are relevant and what agents to invoke.
"""
from __future__ import annotations

import json

from app.core import gemini

SYSTEM = """
You are a routing planner for an AI analytics workspace.
Given a user question and a list of files available in the workspace, you must decide:
1. Which CSV/Excel files (datasets) are needed to answer this question.
2. Which documents (PDFs, DOCX, TXT) are needed.
3. Whether a chart/visualization would meaningfully improve the answer.
4. The type of analysis required.

Return ONLY a JSON object in this exact format:
{
  "intent": "csv_only" | "doc_only" | "hybrid" | "general",
  "csv_file_ids": ["id1", "id2"],
  "doc_file_ids": ["id3"],
  "needs_chart": true | false,
  "chart_hint": "line|bar|scatter|heatmap|histogram|pie|" ,
  "query_type": "stats|trend|comparison|correlation|summary|recommendation|ml|hybrid",
  "reasoning": "brief explanation of why these files were chosen"
}

Rules:
- Only include file IDs that are genuinely required.
- If no files are relevant, return empty arrays and intent "general".
- needs_chart is true only when a visualization clearly adds insight.
- Be conservative with chart hints — only specify when obvious.
"""


async def plan(question: str, files: list[dict], history: list[dict]) -> dict:
    """
    files: list of {id, filename, kind, type, columns (for datasets)}
    history: recent conversation turns for context
    """
    history_str = _format_history(history)
    files_str = json.dumps(files, indent=2)

    prompt = f"""
Conversation history (most recent last):
{history_str}

Available workspace files:
{files_str}

User question: {question}

Return the routing JSON now.
"""
    try:
        result = await gemini.generate_json(prompt, system_instruction=SYSTEM)
        return _validate(result)
    except Exception:
        return _fallback(files)


def _validate(result: dict) -> dict:
    return {
        "intent": result.get("intent", "general"),
        "csv_file_ids": result.get("csv_file_ids", []),
        "doc_file_ids": result.get("doc_file_ids", []),
        "needs_chart": bool(result.get("needs_chart", False)),
        "chart_hint": result.get("chart_hint", ""),
        "query_type": result.get("query_type", "general"),
        "reasoning": result.get("reasoning", ""),
    }


def _fallback(files: list[dict]) -> dict:
    csv_ids = [f["id"] for f in files if f.get("kind") == "dataset"]
    doc_ids = [f["id"] for f in files if f.get("kind") == "document"]
    return {
        "intent": "hybrid" if csv_ids and doc_ids else ("csv_only" if csv_ids else "doc_only"),
        "csv_file_ids": csv_ids[:2],
        "doc_file_ids": doc_ids[:2],
        "needs_chart": False,
        "chart_hint": "",
        "query_type": "general",
        "reasoning": "fallback routing — planner could not parse LLM response",
    }


def _format_history(history: list[dict]) -> str:
    if not history:
        return "(no prior conversation)"
    lines = []
    for msg in history[-6:]:
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")[:300]
        lines.append(f"{role}: {content}")
    return "\n".join(lines)
