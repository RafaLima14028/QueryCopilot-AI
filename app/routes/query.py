from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.security import required_role
from app.dependencies.database import get_db

router = APIRouter(
    prefix="/query",
    tags=["query"]
)


@router.post("/preview")
def generate_sql(
    user: dict = Depends(required_role(["admin", "viewer"])),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(user["sub"])

    return user_id


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
