from sqlalchemy import (
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class UserDB(Base):
    __tablename__ = "users_db"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    db_host: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    db_port: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    db_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    db_user: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    db_password_cryp: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="user_db"
    )
