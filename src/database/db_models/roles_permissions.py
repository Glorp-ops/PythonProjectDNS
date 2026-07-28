from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from permissions import Permission
    from roles import Role

# roles_permissions = Table(
#     "roles_permissions",
#     Base.metadata,
#     Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
#     Column(
#         "permission_id",
#         ForeignKey("permissions.id", ondelete="CASCADE"),
#         primary_key=True,
#     ),
# )


class RolesPermissions(Base):
    __tablename__ = "roles_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )

    roles: Mapped[list["Role"]] = relationship(
        back_populates="roles_permissions", uselist=True
    )
    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="roles_permissions", uselist=True
    )
