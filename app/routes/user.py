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
    UserRegisterResponse,
    UserRegiserDbRequest,
    UserRegiserDbResponse
)
from app.dependencies.database import get_db
from app.models.users import User
from app.models.roles import Role
from app.core.security import (
    hash_password,
    verify_token,
    encrypt_password_db
)
from app.models.users_db import UserDB

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
            "is_admin": True
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
    else:
        role_names.append("viewer")

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


@router.post(
    "/register_db",
    response_model=UserRegiserDbResponse
)
async def register_db(
    new_db: UserRegiserDbRequest = Body(
        ...,
        examples={
            "host": "192.168.1.150",
            "port": 5432,
            "db_name": "test_db",
            "user": "user_test",
            "password": "test@123",
            "ssl_mode_enable": True
        }
    ),
    user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    if new_db.host.lower() in ["localhost", "127.0.0.1", "0.0.0.0"]:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Not supported localhost address"
        )

    user_id = int(user.get("sub"))

    user_db = UserDB(
        db_host=new_db.host,
        db_port=new_db.port,
        db_name=new_db.db_name,
        db_user=new_db.user,
        db_password_cryp=encrypt_password_db(
            new_db.password
        ),
        user_id=user_id
    )

    try:
        db.add(user_db)
        await db.commit()
    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

    return UserRegiserDbResponse(
        sucess=True
    )
