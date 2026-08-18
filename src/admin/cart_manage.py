from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Cart


class CartManage(BaseAdminSettings, model=Cart):
    _permission = "carts:manage"
    form_edit_rules: ClassVar[list[str]] = [
        "id",
        "is_active",
        "created_at",
        "updated_at",
    ]
    column_list: ClassVar[list[str]] = [
        "user_id",
        "id",
        "is_active",
        "created_at",
        "updated_at",
    ]
    form_excluded_columns: ClassVar[list[str]] = [
        "created_at",
        "updated_at",
        "carts_items",
        "users",
    ]
