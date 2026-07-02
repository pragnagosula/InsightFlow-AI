from typing import Any
from google import genai
from google.genai import types as genai_types
from app.config import settings

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


async def generate(prompt: str, system_instruction: str | None = None) -> str:
    client = _get_client()
    config = genai_types.GenerateContentConfig(
        system_instruction=system_instruction,
    ) if system_instruction else None
    response = await client.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=config,
    )
    return response.text


async def generate_json(prompt: str, system_instruction: str | None = None) -> Any:
    import json
    import re

    text = await generate(prompt, system_instruction)
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    raw = match.group(1) if match else text
    return json.loads(raw.strip())
