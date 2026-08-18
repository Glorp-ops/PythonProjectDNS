from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Review


class ReviewManage(BaseAdminSettings, model=Review):
    _permission = "reviews:manage"
    column_list: ClassVar[list[str]] = [
        "id",
        "user_id",
        "product_id",
        "rating",
        "title",
        "content",
    ]
    form_excluded_columns: ClassVar[list[str]] = [
        "created_at",
        "updated_at",
        "products",
        "likes",
        "users",
    ]
