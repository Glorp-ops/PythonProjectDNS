from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Computed, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Numeric

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.carts import Cart
    from database.db_models.products import Product


class CartItem(Base):
    __tablename__ = "carts_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL", onupdate="CASCADE"), index=True
    )
    quantity: Mapped[int] = mapped_column(default=1)
    price_at_add: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    total_price = mapped_column(
        Numeric(10, 2), Computed("quantity * price_at_add"), nullable=False
    )

    carts: Mapped[list["Cart"]] = relationship(
        back_populates="carts_items", uselist=True, lazy="raise"
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="carts_items", uselist=True, lazy="raise"
    )
