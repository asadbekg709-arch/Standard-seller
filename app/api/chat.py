import json

from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services import context_builder, prompt_builder
from app.services.openai_client import chat_completion
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    customer = await context_builder.fetch_customer(req.customer_id)
    messages = prompt_builder.build_chat_prompt(customer, req.question)

    raw = await chat_completion(messages, response_format={"type": "json_object"})

    try:
        data = json.loads(raw)
        return ChatResponse(answer=data["answer"])
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Invalid OpenAI response: {e} | raw={raw}")
        raise HTTPException(status_code=502, detail="Invalid AI response format")
