from sqlalchemy import Column, ForeignKey, Table

from src.database.sqlalchemy_connect.base import Base

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
