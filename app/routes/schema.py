from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.security import required_role
from app.services.database_executor import RemoteDatabaseService
from app.services.users_db_service import UserDbService

router = APIRouter(
    prefix="/schema",
    tags=["schema"]
)


@router.get("/")
async def schema(
    user: dict = Depends(required_role(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(user.get("sub"))

    user_db_service = UserDbService(db)
    user_db_data = await user_db_service.get_user_db(user_id)

    if not user_db_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Database not registered"
        )

    remote_db = RemoteDatabaseService(user_db_data)
    result = await remote_db.get_db_schema()

    if not result:
        return {}

    return result
