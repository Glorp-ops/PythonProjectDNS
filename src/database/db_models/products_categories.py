from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from .categories import Category
    from .products import Product


class ProductCategory(Base):
    __tablename__ = "products_categories"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="products_categories", uselist=True
    )
    categories: Mapped[list["Category"]] = relationship(
        back_populates="products_categories", uselist=True
    )
