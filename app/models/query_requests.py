from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from datetime import datetime

from app.core.database import Base


class QueryRequest(Base):
    __tablename__ = "query_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="query_requests"
    )

    session_id: Mapped[str] = mapped_column(String, nullable=False)

    intent_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
