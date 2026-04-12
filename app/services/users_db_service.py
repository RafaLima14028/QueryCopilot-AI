from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users_db import UserDB
from app.core.security import (
    decrypt_password_db
)
from app.schemas.query import UserDbData


class UserDbService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_db(self, user_id: int) -> UserDbData | None:
        result = await self.db.execute(
            select(UserDB)
            .where(UserDB.user_id == user_id)
        )
        row = result.scalars().one_or_none()

        decrypt_password = None

        if row:
            decrypt_password = decrypt_password_db(row.db_password_cryp)
        else:
            return None

        return UserDbData(
            db_name=row.db_name,
            db_password=decrypt_password,
            db_host=row.db_host,
            db_port=row.db_port,
            db_user=row.db_user,
            db_ssl_mode=row.db_ssl_mode
        )
