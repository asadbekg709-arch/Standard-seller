from pydantic import BaseModel


class ChatRequest(BaseModel):
    customer_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str
