from sqlalchemy import (
    String,
    Integer
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    users: Mapped[list["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles"
    )
