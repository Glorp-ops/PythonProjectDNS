from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from src.database.db_models.products import Product


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"), index=True
    )
    image_url: Mapped[str]

    products: Mapped[list["Product"]] = relationship(back_populates="images", uselist=True)
