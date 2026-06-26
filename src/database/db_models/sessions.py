import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base


class Session(MixinReferUser, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    auth_ssid: Mapped[str] = mapped_column(String(64), unique=True)
    refresh_token: Mapped[str] = mapped_column(String(64), unique=True)
    auth_public_uid: Mapped[str] = mapped_column(String(64), unique=True)
    user_agent: Mapped[str]
    ip: Mapped[str]
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    _ondelete = "CASCADE"
    _create_at = True
    _user_back_populates = "sessions"
