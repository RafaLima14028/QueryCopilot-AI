from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.services.sql_generate_services import SqlGenerateServices

from app.dependencies.security import required_role
from app.dependencies.database import get_db
from app.models.sql_generate import SqlGenerate
from app.schemas.history import HistoryResponse

router = APIRouter(
    prefix="/history",
    tags=["history"]
)


@router.get(
    "/",
    response_model=list[HistoryResponse]
)
async def history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(user.get("sub"))

    rows = await SqlGenerateServices(db).get_n_executions(
        user_id=user_id,
        skip=skip,
        limit=limit
    )

    for row in rows:
        if isinstance(row.sql_json, str):
            row.sql_json = json.loads(row.sql_json)

    return rows


@router.get(
    "/{id}",
    response_model=HistoryResponse
)
async def history_by_id(
    id: int = Path(...),
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(user.get("sub"))

    row = await SqlGenerateServices(db).get_by_id(
        user_id=user_id,
        id=id
    )

    if isinstance(row.sql_json, str):
        row.sql_json = json.loads(row.sql_json)

    return row
