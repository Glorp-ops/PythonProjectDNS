from typing import TYPE_CHECKING
from ..sqlalchemy_connect.base import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .products import Product
    from .categories import Category


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
