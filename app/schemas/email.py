from pydantic import BaseModel
from typing import Literal


class EmailRequest(BaseModel):
    customer_id: str
    tone: Literal["formal", "friendly", "sales"] = "formal"
    language: Literal["en", "ru", "uz"] = "en"


class EmailResponse(BaseModel):
    subject: str
    body: str
