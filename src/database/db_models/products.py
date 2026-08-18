from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from .carts_items import CartItem
    from .favorites import Favorite
    from .images import Image
    from .order_items import OrderItem
    from .products_categories import ProductCategory
    from .reviews import Review


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    price: Mapped[Decimal]
    quantity: Mapped[int]
    description: Mapped[str | None] = mapped_column(default=None)
    review_count: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float] = mapped_column(default=0.0)
    sku: Mapped[str] = mapped_column(default=uuid4().hex.split("-")[0])
    active_at: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=UTC),
        server_default=func.now(),
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)

    images: Mapped[list["Image"]] = relationship(back_populates="products", uselist=True)
    carts_items: Mapped[list["CartItem"]] = relationship(
        back_populates="products", uselist=True
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="products", uselist=True
    )
    reviews: Mapped[list["Review"]] = relationship(back_populates="products", uselist=True)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="products", uselist=True)

    products_categories: Mapped[list["ProductCategory"]] = relationship(
        back_populates="products", uselist=True
    )

    __table_args__ = (
        CheckConstraint("price > 0", name="product_price"),
        CheckConstraint("quantity >= 0", name="product_quantity"),
        CheckConstraint("rating >= 0 and rating <= 5", name="product_rating"),
        CheckConstraint("review_count >= 0", name="product_review_count"),
    )
