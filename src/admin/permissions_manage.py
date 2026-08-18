from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Permission


class PermissionManage(BaseAdminSettings, model=Permission):
    _permission = "permissions:manage"
    column_list: ClassVar[list[str]] = ["id", "name"]
    form_excluded_columns: ClassVar[list[str]] = ["roles_permissions"]
