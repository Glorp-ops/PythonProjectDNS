from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import UserRole


class UserRoleManage(BaseAdminSettings, model=UserRole):
    _permission = "users_roles:manage"

    column_list: ClassVar[list[str]] = ["user_id", "role_id"]
    form_excluded_columns: ClassVar[list[str]] = ["users", "roles"]
    form_edit_rules: ClassVar[list[str]] = ["role_id"]
