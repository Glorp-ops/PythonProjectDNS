from typing import ClassVar

from ..admin import BaseAdminSettings

from ..database.db_models import Like


class LikeManage(BaseAdminSettings, model=Like):
    _permission = "likes:manage"

    column_list: ClassVar[list[str]] = ["id", "user_id", "review_id", "created_at"]
    form_excluded_columns: ClassVar[list[str]] = ["created_at", "users", "reviews"]
    form_edit_rules: ClassVar[list[str]] = ["id", "review_id"]
