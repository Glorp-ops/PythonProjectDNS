from typing import ClassVar

from ..admin import BaseAdminSettings

from ..database.db_models import RolesPermissions


class RolesPermissionsManage(BaseAdminSettings, model=RolesPermissions):
    _permission = "roles_permissions:manage"

    column_list: ClassVar[list[str]] = ["permission_id", "role_id"]
    form_excluded_columns: ClassVar[list[str]] = ["permissions", "roles"]
