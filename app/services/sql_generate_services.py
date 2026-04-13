from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, update

from app.models.sql_generate import SqlGenerate
from app.ai.schemas.sql_generator_agent import SqlGeneratorResponse


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

    async def get_n_executions(
        self,
        user_id: int,
        skip: int,
        limit: int
    ) -> list[SqlGenerate]:
        result = await self.db.execute(
            select(SqlGenerate)
            .where(
                SqlGenerate.user_id == user_id,
                SqlGenerate.executed.is_(True)
            )
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()

    async def get_by_id(
        self,
        user_id: int,
        id: int
    ) -> SqlGenerate | None:
        result = await self.db.execute(
            select(SqlGenerate)
            .where(
                SqlGenerate.user_id == user_id,
                SqlGenerate.executed.is_(True),
                SqlGenerate.id == id
            )
        )
        return result.scalar_one_or_none()

    async def insert(
        self,
        user_id: int,
        response_sql: SqlGeneratorResponse
    ) -> bool:
        try:
            self.db.add(
                SqlGenerate(
                    user_id=user_id,
                    sql_json=response_sql.model_dump_json(exclude_none=True),
                    executed=False,
                )
            )
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}"
            )

        return True
