from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserRegiserDbRequest,
    UserRegiserDbResponse
)
from app.dependencies.database import get_db
from app.core.security import (
    verify_token,
    encrypt_password_db
)
from app.models.users_db import UserDB

from app.services.user_services import UserServices
from app.services.role_services import RoleServices
from app.services.users_db_service import UserDbService

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
    user_service = UserServices(db)
    user_exists = user_service.get_by_email(new_user.email)

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

    role_services = RoleServices(db)
    roles_found = await role_services.get_roles(role_names)

    id, name, email = await user_service.insert_new_user(
        name=new_user.name,
        email=new_user.email,
        password=new_user.password,
        roles_found=roles_found
    )

    return UserRegisterResponse(
        id=id,
        name=name,
        email=email
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

    user_db_service = UserDbService(db)
    await user_db_service.insert_new_user_db(
        new_db.host,
        new_db.port,
        new_db.db_name,
        new_db.user,
        new_db.password,
        new_db.ssl_mode_enable,
        user_id=user_id
    )

    return UserRegiserDbResponse(
        sucess=True
    )
