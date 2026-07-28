from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.mixin_models.mixin_refer_users import MixinReferUser
from src.database.sqlalchemy_connect.base import Base

if TYPE_CHECKING:
    from database.db_models.order_items import OrderItem


class Order(MixinReferUser, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(25), default="собирается", server_default="собирается")
    delivery_address: Mapped[str]
    delivery_method: Mapped[str] = mapped_column(String(25))
    total_price: Mapped[Decimal]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )

    _user_back_populates = "orders"
    _use_list = True

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="orders", uselist=True
    )

    __table_args__ = (CheckConstraint("total_price  > 0", name="orders_total_price"),)
