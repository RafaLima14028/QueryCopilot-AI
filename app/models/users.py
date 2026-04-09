from sqlalchemy import (
    String,
    Integer,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from datetime import datetime

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
