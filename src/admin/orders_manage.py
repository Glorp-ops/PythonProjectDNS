from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Order


class OrderManage(BaseAdminSettings, model=Order):
    _permission = "orders:manage"

    column_list: ClassVar[list[str]] = [
        "id",
        "user_id",
        "status",
        "delivery_address",
        "delivery_method",
        "total_price",
        "created_at",
    ]

    form_excluded_columns: ClassVar[list[str]] = [
        "created_at",
        "total_price",
        "order_items",
        "users",
    ]
    form_edit_rules: ClassVar[list[str]] = [
        "id",
        "status",
        "delivery_address",
        "delivery_method",
    ]
