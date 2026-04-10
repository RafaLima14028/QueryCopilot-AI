from fastapi import (
    APIRouter,
    Depends,
    Body,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.security import required_role
from app.dependencies.database import get_db
from app.schemas.query import (
    QueryPreviewRequest,
    QueryPreviewResponse
)
from app.ai.agents.intent_agent import create_intent_agent
from app.ai.schemas.intent_agent import SemanticIntent
from app.models.query_requests import QueryRequest

router = APIRouter(
    prefix="/query",
    tags=["query"]
)


@router.post("/preview", response_model=QueryPreviewResponse)
async def generate_sql(
    query: QueryPreviewRequest = Body(
        ...,
        examples={
            "text": "It includes all users who made a purchase in the last month.",
            "session_id": "8f7c2b3e-9a41-4d6a-8f0a-2b6d9e5c7a12"
        }
    ),
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(user["sub"])

    intent_agent = create_intent_agent()

    try:
        response = await intent_agent.arun(
            input=query.text,
            user_id=str(user_id),
            session_id=query.session_id,
            stream=False
        )

        intent: SemanticIntent = response.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

    if not intent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent's empty response"
        )

    if intent.needs_clarification is True or intent.confidence < 0.8:
        return QueryPreviewResponse(
            is_question=True,
            question=intent.clarification_question
        )

    query_req = QueryRequest(
        user_id=user_id,
        session_id=query.session_id,
        intent_json=intent.model_dump_json(exclude_none=True)
    )

    try:
        db.add(query_req)
        await db.commit()
    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

    return QueryPreviewResponse(
        is_question=False
    )


@router.post("/execute")
def execute_sql(
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db)
):
    pass


@router.post("/confirm")
def generate_sql(
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db)
):
    pass
