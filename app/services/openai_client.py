import time
from typing import Any

from openai import AsyncOpenAI, APITimeoutError, APIError

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_client: AsyncOpenAI | None = None


def get_openai_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        settings = get_settings()
        _client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.timeout,
            max_retries=2,
        )
    return _client


async def chat_completion(
    messages: list[dict],
    response_format: dict | None = None,
    max_tokens: int = 1000,
) -> str:
    settings = get_settings()
    client = get_openai_client()

    kwargs: dict[str, Any] = {
        "model": settings.openai_model,
        "messages": messages,
        "max_tokens": max_tokens,
    }
    if response_format:
        kwargs["response_format"] = response_format

    start = time.monotonic()
    try:
        response = await client.chat.completions.create(**kwargs)
        elapsed = round(time.monotonic() - start, 3)
        usage = response.usage
        logger.info(
            f"OpenAI call OK | model={settings.openai_model} "
            f"tokens={usage.total_tokens if usage else '?'} time={elapsed}s"
        )
        return response.choices[0].message.content or ""
    except APITimeoutError:
        logger.error("OpenAI request timed out")
        raise
    except APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise
