from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Body
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import (
    verify_password,
    create_acess_token
)
from app.dependencies.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse
)
from app.models.users import User

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
    user_db = (await db.scalars(
        select(User).where(User.email == user.email)
    )).first()

    if not user_db or not verify_password(user.password, user_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_acess_token({"sub": str(user_db.id)})

    return LoginResponse(token=token)
