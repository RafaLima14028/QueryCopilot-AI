from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.roles import Role


class RoleServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_roles(
        self,
        role_names: list[str]
    ) -> list[Role]:
        query_roles = await self.db.execute(
            select(Role)
            .where(Role.name.in_(role_names))
        )
        return query_roles.scalars().all()
