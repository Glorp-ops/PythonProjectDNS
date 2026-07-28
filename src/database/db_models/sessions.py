from datetime import UTC, datetime
from hashlib import sha256
from secrets import token_urlsafe

from sqlalchemy import TIMESTAMP, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.config import settings
from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base


class Session(MixinReferUser, Base):
    id: Mapped[str] = mapped_column(
        String(64), primary_key=True, default=lambda: token_urlsafe(16)
    )
    auth_ssid: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        default=lambda: sha256(token_urlsafe(32).encode()).hexdigest(),
    )
    refresh_token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        default=lambda: sha256(token_urlsafe(32).encode()).hexdigest(),
    )
    user_agent: Mapped[str]
    ip: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=settings.settings_jwt.EXPIRATION_SESSION
    )
    revoked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz=UTC),
        server_default=func.now(),
    )
    update: Mapped[bool] = mapped_column(default=False)

    _ondelete = "CASCADE"
    _create_at = True
    _user_back_populates = "sessions"
