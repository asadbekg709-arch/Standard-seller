import json

from fastapi import APIRouter, HTTPException

from app.schemas.summary import SummaryRequest, SummaryResponse
from app.services import prompt_builder
from app.services.cache_service import cache_get, cache_set, make_cache_key
from app.services.openai_client import chat_completion
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("", response_model=SummaryResponse)
async def summarize(req: SummaryRequest) -> SummaryResponse:
    cache_key = make_cache_key("summary", {"text": req.text})
    cached = await cache_get(cache_key)
    if cached:
        logger.info(f"Cache hit: {cache_key}")
        return SummaryResponse(**cached)

    messages = prompt_builder.build_summary_prompt(req.text)
    raw = await chat_completion(
        messages,
        response_format={"type": "json_object"},
        max_tokens=1500,
    )

    try:
        data = json.loads(raw)
        result = SummaryResponse(
            summary=data["summary"],
            action_items=data.get("action_items", []),
            key_points=data.get("key_points", []),
        )
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Invalid OpenAI response: {e} | raw={raw}")
        raise HTTPException(status_code=502, detail="Invalid AI response format")

    await cache_set(cache_key, result.model_dump())
    return result
