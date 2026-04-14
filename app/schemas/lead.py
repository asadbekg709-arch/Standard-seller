from pydantic import BaseModel
from typing import Literal


class LeadRequest(BaseModel):
    customer_id: str


class LeadResponse(BaseModel):
    score: int
    priority: Literal["low", "medium", "high"]
    reason: str
