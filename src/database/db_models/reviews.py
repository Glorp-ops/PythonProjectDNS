from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.likes import Like
    from database.db_models.products import Product


class Review(MixinReferUser, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    rating: Mapped[float]
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=UTC),
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=UTC),
        server_default=func.now(),
    )

    products: Mapped[list["Product"]] = relationship(back_populates="reviews", uselist=True)

    likes: Mapped[list["Like"]] = relationship(back_populates="reviews", uselist=True)

    _user_back_populates = "reviews"
    _use_list = True
    _ondelete = "CASCADE"

    __table_args__ = (
        CheckConstraint("rating >= 0 and rating <= 5", name="review_rating"),
        UniqueConstraint(
            "user_id", "product_id", name="unique_product_id_user_id_for_reviews"
        ),
    )
