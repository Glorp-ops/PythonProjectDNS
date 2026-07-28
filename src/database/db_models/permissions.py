from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models import RolesPermissions


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    roles_permissions: Mapped[list["RolesPermissions"]] = relationship(
        back_populates="permissions", uselist=True
    )
