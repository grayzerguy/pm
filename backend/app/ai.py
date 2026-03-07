import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPEN_ROUTE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENROUTER_MODEL = "openai/gpt-oss-120b"
OPENAI_MODEL = "gpt-4o-mini"


def call_ai(messages: list) -> str:
    # try OpenRouter first; fall back to OpenAI on payment/auth errors
    if OPENROUTER_API_KEY:
        try:
            return _call(
                "https://openrouter.ai/api/v1/chat/completions",
                OPENROUTER_API_KEY,
                OPENROUTER_MODEL,
                messages,
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code not in (401, 402, 403):
                raise
            # fall through to OpenAI

    if OPENAI_API_KEY:
        return _call(
            "https://api.openai.com/v1/chat/completions",
            OPENAI_API_KEY,
            OPENAI_MODEL,
            messages,
        )

    raise ValueError("No valid AI API key configured")


def _call(url: str, api_key: str, model: str, messages: list) -> str:
    with httpx.Client(timeout=30) as client:
        resp = client.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages},
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
