from pydantic import BaseModel
from typing import Union


class SqlGeneratorResponse(BaseModel):
    sql: str
    params: list[Union[str, int, float, bool]] = []
    explanation: str
