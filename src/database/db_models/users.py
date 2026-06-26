import uuid
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_models.users_roles import users_roles_table
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from roles import Role

    from src.database.db_models.sessions import Session


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str | None] = mapped_column(String(25))
    nickname: Mapped[str] = mapped_column(String(25), unique=True)
    number_phone: Mapped[str | None] = mapped_column(String(15), unique=True)
    email: Mapped[str | None] = mapped_column(unique=True)
    password: Mapped[str | None] = mapped_column(String(25), unique=True)
    active_at: Mapped[bool] = mapped_column(default=True)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="users", uselist=True
    )
    roles: Mapped[list["Role"]] = relationship(
        back_populates="users", secondary=users_roles_table, uselist=True
    )
