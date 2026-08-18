from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Category


class CategoryManage(BaseAdminSettings, model=Category):
    _permission = "categories:manage"

    column_list: ClassVar[list[str]] = ["id", "name", "slug", "parent_id"]

    form_excluded_columns: ClassVar[list[str]] = ["products", "parent", "products_categories"]
