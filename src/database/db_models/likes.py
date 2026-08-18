from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.reviews import Review


class Like(MixinReferUser, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(
        ForeignKey("reviews.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=UTC),
        server_default=func.now(),
    )

    reviews: Mapped[list["Review"]] = relationship(back_populates="likes", uselist=True)

    _use_list = True
    _user_back_populates = "likes"
    _ondelete = "CASCADE"

    __table_args__ = (
        UniqueConstraint("user_id", "review_id", name="unique_review_id_user_id"),
        Index("idx_user_review_id", "user_id", "review_id"),
    )
