from typing import Any, ClassVar

from starlette.requests import Request

from ..database.db_models import Blacklist
from ..database.repositories_db import SessionRepository, UserRepository
from ..database.sqlalchemy_connect import async_session
from .base_settings_admin_models import BaseAdminSettings


class BlackListManage(BaseAdminSettings, model=Blacklist):
    column_list: ClassVar[list[str]] = ["user_id", "reason", "ban_until", "created_at"]
    form_excluded_columns: ClassVar[list[str]] = ["created_at", "users"]
    form_edit_rules: ClassVar[list[str]] = ["reason", "ban_until", "created_at"]

    _permission = "blacklists:manage"

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        user_id = data.get("user_id")

        if is_created:
            async with async_session() as session:
                await UserRepository(session).update(user_id, is_blocked=True)
                await SessionRepository(session).delete(user_id=user_id)

    async def delete_model(self, request: Request, pk: Any) -> None:

        async with async_session() as session:
            await UserRepository(session).update(pk, is_blocked=False)

        await super().delete_model(request, pk)
