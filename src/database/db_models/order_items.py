from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.orders import Order
    from database.db_models.products import Product


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int]
    price_at_purchase: Mapped[Decimal]

    orders: Mapped[list["Order"]] = relationship(back_populates="order_items", uselist=True)
    products: Mapped[list["Product"]] = relationship(
        back_populates="order_items", uselist=True
    )

    __table_args__ = (
        CheckConstraint("price_at_purchase > 0", name="order_items_price_at_purchase"),
        CheckConstraint("quantity > 0", name="order_quantity"),
    )
