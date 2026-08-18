from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Product


class ProductManage(BaseAdminSettings, model=Product):
    _permission = "products:manage"

    column_list: ClassVar[list[str]] = [
        "id",
        "name",
        "description",
        "price",
        "quantity",
        "review_count",
        "rating",
        "sku",
        "active_at",
        "created_at",
        "is_deleted",
    ]

    form_excluded_columns: ClassVar[list[str]] = [
        "sku",
        "created_at",
        "categories",
        "images",
        "carts_items",
        "order_items",
        "reviews",
        "favorites",
        "products_categories",
    ]
