from fastapi import HTTPException, status

from app.ai.agents.intent_agent import create_intent_agent
from app.ai.schemas.intent_agent import SemanticIntent
from app.schemas.query import (
    QueryPreviewResponse
)
from app.schemas.query import UserDbData
from app.ai.agents.sql_generator_agent import create_sql_generator_agent
from app.ai.schemas.sql_generator_agent import SqlGeneratorResponse


class AiAgentsService:
    def __init__(
        self, user_id: int, user_roles: list, session_id: str
    ):
        self.user_id = user_id
        self.session_id = session_id
        self.user_roles = user_roles

    async def intent_agent(
        self, input_user: str
    ) -> QueryPreviewResponse | SemanticIntent:
        agent = create_intent_agent()

        try:
            response = await agent.arun(
                input=input_user,
                user_id=str(self.user_id),
                session_id=self.session_id,
                stream=False,
                dependencies={"user_roles": self.user_roles},
            )

            intent: SemanticIntent = response.content
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}",
            )

        if not intent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agent's empty response",
            )

        if intent.confidence < 0.8 and intent.clarification_question:
            return QueryPreviewResponse(
                is_question=True,
                question=intent.clarification_question
            )

        return intent

    async def sql_generator_agent(
        self, user_db: UserDbData, intent: SemanticIntent
    ) -> SqlGeneratorResponse:
        sql_agent = create_sql_generator_agent(user_db)

        response = await sql_agent.arun(
            input=intent,
            user_id=str(self.user_id),
            session_id=self.session_id,
            stream=False
        )

        response_sql: SqlGeneratorResponse = response.content

        return response_sql
