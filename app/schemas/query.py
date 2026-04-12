from pydantic import BaseModel
from typing import Optional


class QueryPreviewRequest(BaseModel):
    text: str
    session_id: str


class QueryPreviewResponse(BaseModel):
    is_question: bool = False
    question: Optional[str] = None


class UserDbData(BaseModel):
    db_name: str
    db_password: str
    db_host: str
    db_port: int
    db_user: str
