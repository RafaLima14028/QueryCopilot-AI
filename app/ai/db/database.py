from agno.db.postgres import AsyncPostgresDb

from app.core.security import get_settings

settings = get_settings()

db = AsyncPostgresDb(
    db_url=settings.DATABASE_URL
)
