from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.models.users_db import UserDB
from app.core.security import encrypt_password_db
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

        if not row:
            return None

        return UserDbData(
            db_name=row.db_name,
            db_password=row.db_password_cryp,
            db_host=row.db_host,
            db_port=row.db_port,
            db_user=row.db_user,
            db_ssl_mode=row.db_ssl_mode
        )

    async def get_user_db_or_error(
        self, user_id: int
    ) -> UserDbData:
        try:
            result = await self.db.execute(
                select(UserDB)
                .where(UserDB.user_id == user_id)
            )
            data = result.scalars().one()

            return UserDbData(
                db_name=data.db_name,
                db_password=data.db_password_cryp,
                db_host=data.db_host,
                db_port=data.db_port,
                db_user=data.db_user,
                db_ssl_mode=data.db_ssl_mode
            )
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No database registered",
            )

    async def insert_new_user_db(
        self,
        db_host: str,
        db_port: int,
        db_name: str,
        db_user: str,
        db_password: str,
        db_ssl_mode: str,
        user_id: int
    ):
        user_db = UserDB(
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            db_user=db_user,
            db_password_cryp=encrypt_password_db(
                db_password
            ),
            db_ssl_mode=db_ssl_mode,
            user_id=user_id
        )

        try:
            self.db.add(user_db)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}"
            )
