from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, update

from app.models.sql_generate import SqlGenerate


class SqlGenerateServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_last(self, user_id: int) -> bool:
        last_query = await self.get_last(user_id)

        await self.db.execute(
            update(SqlGenerate)
            .where(
                SqlGenerate.user_id == user_id,
                SqlGenerate.id == last_query.id
            )
            .values(
                executed=True
            )
        )
        await self.db.commit()

        return True

    async def get_last(self, user_id: int) -> dict:
        result = await self.db.execute(
            select(SqlGenerate)
            .where(
                SqlGenerate.user_id == user_id,
            )
            .order_by(desc(SqlGenerate.created_at))
            .limit(1)
        )

        row = result.scalars().one_or_none()

        if row is None:
            return {}

        return row
