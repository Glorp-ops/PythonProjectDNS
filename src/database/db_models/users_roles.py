from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from src.database.db_models.roles import Role
    from src.database.db_models.users import User


class UserRole(Base):
    __tablename__ = "users_roles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )

    users: Mapped[list["User"]] = relationship(back_populates="users_roles", uselist=True)
    roles: Mapped[list["Role"]] = relationship(back_populates="users_roles", uselist=True)
