import asyncio
import json

from fastapi import APIRouter, HTTPException

from app.schemas.lead import LeadRequest, LeadResponse
from app.services import context_builder, prompt_builder
from app.services.cache_service import cache_get, cache_set, make_cache_key
from app.services.openai_client import chat_completion
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/score", response_model=LeadResponse)
async def score_lead(req: LeadRequest) -> LeadResponse:
    cache_key = make_cache_key("lead", {"cid": req.customer_id})
    cached = await cache_get(cache_key)
    if cached:
        logger.info(f"Cache hit: {cache_key}")
        return LeadResponse(**cached)

    customer, orders, activities = await asyncio.gather(
        context_builder.fetch_customer(req.customer_id),
        context_builder.fetch_orders(req.customer_id),
        context_builder.fetch_activities(req.customer_id),
    )

    messages = prompt_builder.build_lead_prompt(customer, orders, activities)
    raw = await chat_completion(messages, response_format={"type": "json_object"})

    try:
        data = json.loads(raw)
        result = LeadResponse(
            score=int(data["score"]),
            priority=data["priority"],
            reason=data["reason"],
        )
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Invalid OpenAI response: {e} | raw={raw}")
        raise HTTPException(status_code=502, detail="Invalid AI response format")

    await cache_set(cache_key, result.model_dump(), ttl=1800)
    return result
