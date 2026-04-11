from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    Boolean
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)
from sqlalchemy.dialects.postgresql import (
    JSONB
)
from datetime import datetime

from app.core.database import Base


class SqlGenerate(Base):
    __tablename__ = "sql_generate"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="sql_generate"
    )

    sql_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    executed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
