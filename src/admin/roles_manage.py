from typing import ClassVar

from ..admin import BaseAdminSettings

from ..database.db_models import Role


class RoleManage(BaseAdminSettings, model=Role):
    _permission = "roles:manage"
    column_list: ClassVar[list[str]] = ["id", "name", "parent_id"]
    form_excluded_columns: ClassVar[list[str]] = [
        "roles_permissions",
        "users_roles",
        "parent",
    ]
