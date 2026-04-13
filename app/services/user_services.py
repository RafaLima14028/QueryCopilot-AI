from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import User
from app.models.roles import Role
from app.core.security import hash_password


class UserServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert_new_user(
        self,
        name: str,
        email: str,
        password: str,
        roles_found: list[Role]
    ) -> tuple[int, str, str]:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password)
        )

        user.roles.extend(roles_found)

        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(
                user,
                attribute_names=["roles"]
            )
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}"
            )

        return user.id, user.name, user.email

    async def get_by_email(
        self, email: str
    ) -> User | None:
        query_user = await self.db.execute(
            select(User)
            .where(User.email == email)
        )
        return query_user.scalar_one_or_none()
