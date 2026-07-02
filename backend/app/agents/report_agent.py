"""
Report Agent — generates a structured PDF report from analysis results.
"""
from __future__ import annotations

from app.core import gemini

SYSTEM = """
You are a business report writer. Given the user's question and the analysis context,
write a professional business report in markdown format.

Structure the report as:
# Executive Summary
(2-3 sentences)

# Key Findings
(bullet points with specific data)

# Analysis
(detailed section with numbers and trends)

# Recommendations
(actionable items)

# Conclusion
(brief wrap-up)

Be factual, data-driven, and professional.
"""


async def generate_report_content(question: str, fused_context: str, title: str) -> str:
    prompt = f"""
Report Title: {title}
Original Question: {question}

Analysis Context:
{fused_context}

Write the full business report now.
"""
    return await gemini.generate(prompt, system_instruction=SYSTEM)
