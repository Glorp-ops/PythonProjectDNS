from sqlalchemy import UUID, Column, ForeignKey, Integer, Table

from src.database.sqlalchemy_connect.base import Base

users_roles_table = Table(
    "users_roles",
    Base.metadata,
    Column(
        "user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    ),
)
