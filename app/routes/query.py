from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import json

from app.dependencies.security import required_role
from app.dependencies.database import get_db
from app.schemas.query import (
    QueryPreviewRequest,
    QueryPreviewResponse,
)
from app.ai.schemas.sql_generator_agent import SqlGeneratorResponse
from app.services.database_executor import RemoteDatabaseService
from app.services.sql_generate_services import SqlGenerateServices
from app.services.database_executor import RemoteDatabaseService

from app.services.ai_agents_service import AiAgentsService
from app.services.query_requests_service import QueryRequetsService
from app.services.users_db_service import UserDbService

router = APIRouter(prefix="/query", tags=["query"])


@router.post(
    "/preview",
    response_model=QueryPreviewResponse | SqlGeneratorResponse
)
async def generate_sql(
    query: QueryPreviewRequest = Body(
        ...,
        examples={
            "text": "It includes all users who made a purchase in the last month.",
            "session_id": "8f7c2b3e-9a41-4d6a-8f0a-2b6d9e5c7a12",
        },
    ),
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(user["sub"])
    user_roles: list = user.get("roles", [])

    agents = AiAgentsService(
        user_id, user_roles, query.session_id
    )
    intent = await agents.intent_agent(
        query.text
    )

    if isinstance(intent, QueryPreviewResponse) and intent.is_question:
        return intent

    query_req_service = QueryRequetsService(db)
    await query_req_service.insert(
        user_id,
        query.session_id,
        intent
    )

    user_db_service = UserDbService(db)
    user_db_data = await user_db_service.get_user_db_or_error(
        user_id
    )

    response_sql = await agents.sql_generator_agent(
        user_db_data,
        intent
    )

    sql_service = SqlGenerateServices(db)
    await sql_service.insert(user_id, response_sql)

    return response_sql


@router.post("/execute")
async def execute_sql(
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(user.get("sub"))

    sql_service = SqlGenerateServices(db)
    last_sql_not_executed = await sql_service.get_last(user_id)
    data = last_sql_not_executed.sql_json

    if not last_sql_not_executed:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"There are no pending SQL queries"
        )
    elif last_sql_not_executed.executed == True:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"There are no pending SQL queries"
        )
    elif isinstance(data, str):
        data = json.loads(data)

    user_db_service = UserDbService(db)
    user_db_data = await user_db_service.get_user_db(user_id)

    if not user_db_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Database not registered"
        )

    remote_db = RemoteDatabaseService(user_db_data)
    rows_db_user = await remote_db.execute_query(
        query=data["sql"],
        params=data["params"],
    )

    await sql_service.update_last(user_id)

    return rows_db_user
