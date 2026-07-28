from typing import Any, ClassVar

from bcrypt import gensalt, hashpw
from starlette.requests import Request

from ..admin import BaseAdminSettings

from ..database.db_models import User


class UserManage(BaseAdminSettings, model=User):
    column_list: ClassVar[list[str]] = [
        "id",
        "nickname",
        "name",
        "surname",
        "email",
        "is_active",
        "is_blocked",
    ]

    form_excluded_columns: ClassVar[list[str]] = [
        "sessions",
        "users_roles",
        "carts",
        "blacklists",
        "orders",
        "reviews",
        "favorites",
        "likes",
    ]
    _permission = "users:manage"

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        password: str = data.get("password")
        #
        if is_created or password != model.password:
            data.update({"password": hashpw(password.encode(), gensalt()).hex()})
