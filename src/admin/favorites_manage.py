from typing import ClassVar

from ..admin import BaseAdminSettings

from ..database.db_models import Favorite


class FavoritesManage(BaseAdminSettings, model=Favorite):
    _permission = "favorites:manage"
    column_list: ClassVar[list[str]] = ["id", "user_id", "product_id", "created_at"]
    form_excluded_columns: ClassVar[list[str]] = ["created_at", "products", "users"]
    form_edit_rules: ClassVar[list[str]] = ["id", "product_id"]
