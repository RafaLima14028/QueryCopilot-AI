from pydantic import BaseModel
from typing import Optional


class QueryPreviewRequest(BaseModel):
    text: str
    session_id: str


class QueryPreviewResponse(BaseModel):
    is_question: bool = False
    question: Optional[str] = None
