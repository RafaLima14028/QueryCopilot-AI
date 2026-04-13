from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.users import User
from app.core.security import (
    verify_password,
    create_acess_token
)
from app.schemas.auth import (
    LoginRequest
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_user_and_roles(
        self, user_email: str
    ) -> User | None:
        query = (
            select(User)
            .where(User.email == user_email)
            .options(selectinload(User.roles))
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    def _create_jwt_token(
        self, user_id: int, user_roles: list[str]
    ) -> str:
        return create_acess_token({
            "sub": str(user_id),
            "roles": user_roles
        })

    async def login(self, user: LoginRequest) -> str:
        user_db = await self._get_user_and_roles(user.email)

        if not user_db or not verify_password(user.password, user_db.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        return self._create_jwt_token(
            user_id=user_db.id,
            user_roles=[role.name for role in user_db.roles]
        )
