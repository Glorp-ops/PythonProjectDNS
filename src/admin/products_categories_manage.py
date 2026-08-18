from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import ProductCategory


class ProductCategoryManage(BaseAdminSettings, model=ProductCategory):
    _permission = "products_categories:manage"

    column_list: ClassVar[list[str]] = ["product_id", "category_id"]
    form_excluded_columns: ClassVar[list[str]] = ["products", "categories"]
