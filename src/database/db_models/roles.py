from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_models.users_roles import UserRole
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from users_roles import UserRole

    from src.database.db_models.roles_permissions import RolesPermissions


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    # permissions: Mapped[list["Permission"]] = relationship(
    #     back_populates="roles", secondary=RolesPermissions, uselist=True
    # )

    roles_permissions: Mapped[list[RolesPermissions]] = relationship(
        back_populates="roles", uselist=True
    )
    users_roles: Mapped[list["UserRole"]] = relationship(back_populates="roles", uselist=True)
    parent: Mapped["Role"] = relationship(remote_side=[id])

    # users: Mapped[list["User"]] = relationship(
    #     back_populates="roles", secondary=users_roles, uselist=True
    # )
