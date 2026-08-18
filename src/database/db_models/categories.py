from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...database.sqlalchemy_connect import Base

if TYPE_CHECKING:
    from .products_categories import ProductCategory


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL", onupdate="CASCADE"),
        default=None,
    )

    parent: Mapped["Category"] = relationship(remote_side=[id])

    products_categories: Mapped[list["ProductCategory"]] = relationship(
        back_populates="categories", uselist=True
    )
