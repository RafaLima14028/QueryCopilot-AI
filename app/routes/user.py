from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import (
    UserRegisterRequest,
    UserRegisterResponse
)
from app.dependencies.database import get_db
from app.models.users import User
from app.models.roles import Role
from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/register",
    response_model=UserRegisterResponse
)
async def register(
    new_user: UserRegisterRequest = Body(
        ...,
        examples={
            "name": "John",
            "email": "john@test.com",
            "password": "JohnTest123",
            "is_bool": True
        }
    ),
    db: AsyncSession = Depends(get_db)
):
    query_user = await db.execute(
        select(User).where(User.email == new_user.email)
    )
    user_exists = query_user.scalar_one_or_none()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    role_names = []

    if new_user.is_admin:
        role_names.append("admin")

    query_roles = await db.execute(
        select(Role).where(Role.name.in_(role_names))
    )
    roles_found = query_roles.scalars().all()

    user = User(
        name=new_user.name,
        email=new_user.email,
        password_hash=hash_password(new_user.password)
    )

    user.roles.extend(roles_found)

    try:
        db.add(user)
        await db.commit()
        await db.refresh(user, attribute_names=["roles"])
    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

    return UserRegisterResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )
