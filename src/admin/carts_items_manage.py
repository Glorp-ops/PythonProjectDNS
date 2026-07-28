from typing import ClassVar

from ..admin import BaseAdminSettings

from ..database.db_models import CartItem


class CartItemManager(BaseAdminSettings, model=CartItem):
    _permission = "carts_items:manage"
    column_list: ClassVar[list[str]] = [
        "id",
        "product_id",
        "cart_id",
        "quantity",
        "price_at_add",
        "total_price",
    ]

    form_excluded_columns: ClassVar[list[str]] = ["carts", "products"]
