from pydantic import BaseModel
from datetime import datetime


class HistoryResponse(BaseModel):
    id: int
    sql_json: dict
    created_at: datetime
