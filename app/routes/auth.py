from fastapi import (
    APIRouter,
    Depends,
    Body
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService
from app.dependencies.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/login",
    response_model=LoginResponse
)
async def login(
    user: LoginRequest = Body(
        ...,
        examples={
            "email": "john@test.com",
            "paswword": "JohnTest123"
        }
    ),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    token = await auth_service.login(user)

    return LoginResponse(token=token)
