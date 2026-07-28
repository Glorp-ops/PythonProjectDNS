from typing import Any, ClassVar

from starlette.requests import Request

from ..admin import BaseAdminSettings

from ..database.db_models import Session


class SessionManager(BaseAdminSettings, model=Session):
    _permission = "sessions:manage"

    column_list: ClassVar[list[str]] = [
        "user_id",
        "auth_ssid",
        "refresh_token",
        "user_agent",
        "ip",
        "revoked",
        "created_at",
        "updated_at",
        "expires_at",
    ]

    form_excluded_columns: ClassVar[list[str]] = [
        "users",
        "created_at",
        "update",
        "auth_ssid",
        "refresh_token",
        "user_agent",
        "ip",
    ]
    form_create_rules: ClassVar[list[str]] = ["revoked", "expires_at"]
    form_edit_rules: ClassVar[list[str]] = [
        "revoked",
        "expires_at",
    ]

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        user_agent: str = data.get("user_agent")
        ip: str = data.get("ip")

        if is_created or ip != model.ip or user_agent != model.user_agent:
            data.update(
                {
                    "user_agent": request.headers.get("user-agent"),
                    "ip": request.client.host,
                }
            )
