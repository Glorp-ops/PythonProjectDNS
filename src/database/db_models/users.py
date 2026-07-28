import uuid
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.blacklists import Blacklist
    from database.db_models.carts import Cart
    from database.db_models.favorites import Favorite
    from database.db_models.likes import Like
    from database.db_models.orders import Order
    from database.db_models.reviews import Review
    from database.db_models.sessions import Session
    from database.db_models.users_roles import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str | None] = mapped_column(String(25))
    surname: Mapped[str | None] = mapped_column(String(25))
    nickname: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None] = mapped_column(String(150), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)

    sessions: Mapped[list["Session"]] = relationship(back_populates="users", uselist=True)

    users_roles: Mapped[list["UserRole"]] = relationship(back_populates="users", uselist=True)

    carts: Mapped[list["Cart"]] = relationship(back_populates="users", uselist=True)

    blacklists: Mapped["Blacklist"] = relationship(back_populates="users")

    orders: Mapped[list["Order"]] = relationship(back_populates="users", uselist=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="users", uselist=True)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="users", uselist=True)

    likes: Mapped[list["Like"]] = relationship(back_populates="users", uselist=True)

    # roles: Mapped[list["Role"]] = relationship(
    #     back_populates="users", secondary='users_roles', uselist=True
    # )
