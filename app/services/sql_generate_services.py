from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.sql_generate import SqlGenerate


class SqlGenerateServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_last(self, user_id: int) -> dict:
        result = await self.db.execute(
            select(SqlGenerate)
            .where(
                SqlGenerate.user_id == user_id,
                SqlGenerate.executed.is_(False)
            )
            .order_by(desc(SqlGenerate.created_at))
            .limit(1)
        )

        row = result.scalars().one_or_none()

        if row is None:
            return {}

        return row
