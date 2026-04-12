from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from typing import List, Dict, Any
from fastapi import HTTPException, status

from app.models.users_db import UserDB
from app.core.security import decrypt_password_db
from app.schemas.query import UserDbData


class RemoteDatabaseService:
    """
    This service is responsible for connecting to and executing 
    queries on external databases of registered users.
    """

    def __init__(self, user_db: UserDbData):
        self.user_db = user_db

    def _get_connection_url(self) -> str:
        """
        Constructs the connection URL based on the UserDB model data.
        Note: We are using the 'asyncpg' driver for PostgreSQL.
        """

        # postgresql+asyncpg://user:password@host:port/dbname
        return (
            f"postgresql+asyncpg://{self.user_db.db_user}:{self.user_db.db_password}@"
            f"{self.user_db.db_host}:{self.user_db.db_port}/{self.user_db.db_name}"
        )

    async def execute_query(self, query: str, params: list) -> List[Dict[str, Any]]:
        """
        Executes an SQL query, returns the results, and closes the connection.
        Using 'engine.dispose()' ensures that the connection pool is cleared.
        """
        url = self._get_connection_url()

        engine = create_async_engine(url, pool_pre_ping=True)

        try:
            async with engine.connect() as connection:
                placeholders = {}

                for i, val in enumerate(params):
                    placeholder_name = f"p{i}"

                    query = query.replace(
                        "?",
                        f":{placeholder_name}",
                        1
                    )
                    placeholders[placeholder_name] = val

                result = await connection.execute(
                    text(query),
                    placeholders
                )

                # If the query returns rows(SELECT)
                if result.returns_rows:
                    # We return a list of dictionaries to be serializable (JSON).
                    return [dict(row._mapping) for row in result.all()]

                # If it's a DML command (INSERT, UPDATE, DELETE)
                await connection.commit()
                return [{"status": "success", "rows_affected": result.rowcount}]
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error executing query on remote database"
            )
        finally:
            await engine.dispose()
