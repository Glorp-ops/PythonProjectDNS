from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_models.roles import Role
from src.database.db_models.roles_permissions import roles_permissions
from src.database.sqlalchemy_connect.base import Base


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    roles: Mapped["Role"] = relationship(
        back_populates="permissions", secondary=roles_permissions
    )
