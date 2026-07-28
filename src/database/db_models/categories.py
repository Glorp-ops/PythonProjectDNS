from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.products import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL", onupdate="CASCADE"),
        default=None,
    )

    products: Mapped[list["Product"]] = relationship(back_populates="categories", uselist=True)

    parent: Mapped["Category"] = relationship(remote_side=[id])
