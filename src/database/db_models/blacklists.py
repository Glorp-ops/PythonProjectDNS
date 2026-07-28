from datetime import UTC, datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base


class Blacklist(MixinReferUser, Base):
    reason: Mapped[str | None] = mapped_column(String(50), default=None)
    ban_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
    )

    _ondelete = "CASCADE"
    _primary_key = True
    _user_back_populates = "blacklists"
