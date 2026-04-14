import json

from fastapi import APIRouter, HTTPException

from app.schemas.email import EmailRequest, EmailResponse
from app.services import context_builder, prompt_builder
from app.services.cache_service import cache_get, cache_set, make_cache_key
from app.services.openai_client import chat_completion
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/generate", response_model=EmailResponse)
async def generate_email(req: EmailRequest) -> EmailResponse:
    cache_key = make_cache_key(
        "email", {"cid": req.customer_id, "tone": req.tone, "lang": req.language}
    )
    cached = await cache_get(cache_key)
    if cached:
        logger.info(f"Cache hit: {cache_key}")
        return EmailResponse(**cached)

    customer, orders = await _gather_context(req.customer_id)
    messages = prompt_builder.build_email_prompt(customer, orders, req.tone, req.language)

    raw = await chat_completion(messages, response_format={"type": "json_object"})
    try:
        data = json.loads(raw)
        result = EmailResponse(subject=data["subject"], body=data["body"])
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Invalid OpenAI response: {e} | raw={raw}")
        raise HTTPException(status_code=502, detail="Invalid AI response format")

    await cache_set(cache_key, result.model_dump())
    return result


async def _gather_context(customer_id: str) -> tuple[dict, list]:
    import asyncio
    customer, orders = await asyncio.gather(
        context_builder.fetch_customer(customer_id),
        context_builder.fetch_orders(customer_id),
    )
    return customer, orders
