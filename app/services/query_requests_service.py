from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.query_requests import QueryRequest
from app.ai.schemas.intent_agent import SemanticIntent


class QueryRequetsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert(
        self, user_id: int, session_id: str, intent: SemanticIntent
    ) -> bool:
        query_req = QueryRequest(
            user_id=user_id,
            session_id=session_id,
            intent_json=intent.model_dump_json(exclude_none=True),
        )

        try:
            self.db.add(query_req)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}",
            )

        return True
