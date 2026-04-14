from pydantic import BaseModel
from typing import List


class SummaryRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str
    action_items: List[str]
    key_points: List[str]
