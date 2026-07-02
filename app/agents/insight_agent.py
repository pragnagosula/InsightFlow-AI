"""
Insight Agent — calls Gemini with the fused context to produce the final answer.
"""
from __future__ import annotations

from app.core import gemini

SYSTEM = """
You are InsightFlow AI, an expert business intelligence analyst.
You receive structured context containing:
- The user's question
- Results from CSV data analysis (statistics, trends, correlations)
- Retrieved text from uploaded documents (with citations)
- Notes about any generated charts

Your job is to synthesize all of this into a clear, professional answer.

Guidelines:
- Lead with a direct answer to the question.
- Support claims with specific numbers from the CSV analysis when available.
- Reference document sources with their filenames when citing document content.
- If a chart was generated, mention it naturally ("As shown in the chart above...").
- Provide actionable business insights and recommendations when appropriate.
- Use concise, professional language — avoid padding or hedging.
- Format with markdown (headers, bullets, bold) for readability.
- If you don't have enough information, say so clearly and suggest what additional data would help.
"""


async def generate_insight(fused_context: str) -> str:
    try:
        return await gemini.generate(fused_context, system_instruction=SYSTEM)
    except Exception as exc:
        return _fallback_message(exc)


def _fallback_message(exc: Exception) -> str:
    text = str(exc)
    if "RESOURCE_EXHAUSTED" in text or "429" in text:
        reason = "the Gemini API free-tier request quota has been reached for today"
    else:
        reason = "the AI service is temporarily unavailable"
    return (
        f"I couldn't generate a written insight right now because {reason}. "
        "Any chart or data analysis above is still accurate — please try asking again shortly."
    )
