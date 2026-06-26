from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_models.roles_permissions import roles_permissions
from src.database.db_models.users_roles import users_roles_table
from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from permissions import Permission


class Role(MixinReferUser, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="roles", secondary=roles_permissions, uselist=True
    )

    _secondary = users_roles_table
    _user_back_populates = "roles"
