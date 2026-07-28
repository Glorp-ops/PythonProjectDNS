from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)
from typing import TYPE_CHECKING

from ..sqlalchemy_connect import Base
from src.database.db_models.users import User


class MixinReferUser:
    _model_name: Base = User
    _user_id_unique: bool = False
    # _create_at: bool = False
    _user_back_populates: str | None = "sessions"
    _ondelete: str | None = "CASCADE"
    _onupdate: str | None = "NO ACTION"
    _use_list: bool = True
    _secondary: str | None = None
    _primary_key: bool = False
    _index: bool = True

    @declared_attr
    def user_id(self) -> Mapped[UUID]:
        return mapped_column(
            UUID,
            ForeignKey("users.id", ondelete=self._ondelete),
            unique=self._user_id_unique,
            primary_key=self._primary_key,
            index=self._index,
        )

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + "s"

    #
    # @declared_attr
    # def created_at(self) -> Mapped[datetime] | None:
    #     created_at: Mapped[datetime] = mapped_column(
    #         DateTime(timezone=True), default=  datetime.now(UTC)
    #     )
    #     if self._create_at:
    #         return created_at
    #
    #     return None

    @declared_attr
    def users(self) -> Mapped["User"]:
        return relationship(
            User,
            back_populates=self._user_back_populates,
            uselist=self._use_list,
            secondary=self._secondary,
        )
