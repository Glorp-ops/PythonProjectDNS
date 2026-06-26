import datetime
from uuid import UUID

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

from src.database.db_models.users import User
from src.database.sqlalchemy_connect.base import Base


class MixinReferUser:
    _model_name: Base = User
    _user_id_unique: bool = False
    _create_at: bool = False
    _user_back_populates: str | None = "sessions"
    _ondelete: str | None = "CASCADE"
    _onupdate: str | None = "NO ACTION"
    _use_list: bool = True
    _secondary: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[UUID]:
        return mapped_column(
            UUID,
            ForeignKey("users.id", ondelete=cls._ondelete),
            unique=cls._user_id_unique,
        )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    @declared_attr
    def created_at(cls):
        created_at: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), default=datetime.datetime.now
        )
        if cls._create_at:
            return created_at
        return None

    @declared_attr
    def users(cls) -> Mapped["User"]:
        return relationship(
            User,
            back_populates=cls._user_back_populates,
            uselist=cls._use_list,
            secondary=cls._secondary,
        )
