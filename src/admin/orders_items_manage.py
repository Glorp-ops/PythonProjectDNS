from typing import ClassVar

from ..admin import BaseAdminSettings

from ..database.db_models import OrderItem


class OrderItemManage(BaseAdminSettings, model=OrderItem):
    _permission = "orders_items:manage"

    column_list: ClassVar[list[str]] = [
        "id",
        "order_id",
        "product_id",
        "quantity",
        "price_at_purchase",
    ]
    form_excluded_columns: ClassVar[list[str]] = ["orders", "products"]

    can_delete = False
    can_edit = False
