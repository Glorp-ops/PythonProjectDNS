from typing import ClassVar

from ..admin import BaseAdminSettings
from ..database.db_models import Image


class ImageManage(BaseAdminSettings, model=Image):
    _permission = "images:manage"

    column_list: ClassVar[list[str]] = ["id", "product_id", "image_url"]
    form_excluded_columns: ClassVar[list[str]] = ["products"]
