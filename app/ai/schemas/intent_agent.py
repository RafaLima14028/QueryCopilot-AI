from pydantic import BaseModel, Field
from typing import List, Optional


class SemanticFilter(BaseModel):
    field: str
    operator: str
    value: str


class SemanticIntent(BaseModel):
    main_concept: str
    related_concepts: List[str] = []

    action: str

    filters: List[SemanticFilter] = []

    sort: Optional[str] = None
    limit: Optional[int] = None

    confidence: float = Field(..., ge=0, le=1)
    needs_clarification: Optional[bool] = False
    clarification_question: Optional[str] = None
