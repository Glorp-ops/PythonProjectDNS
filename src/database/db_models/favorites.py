from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from src.database.db_models.products import Product


class Favorite(Base, MixinReferUser):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        server_default=func.now(),
    )

    products: Mapped[list["Product"]] = relationship(back_populates="favorites", uselist=True)

    _user_back_populates = "favorites"
    _use_list = True

    __table_args__ = (
        UniqueConstraint("product_id", "user_id", name="unique_product_id_user_id"),
        Index("ix_favorites_user_id", "user_id"),
    )
