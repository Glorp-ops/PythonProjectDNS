from typing import Any
from uuid import UUID

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.repositories_db import (
    RoleRepository,
    SessionRepository,
    UserRepository,
    UserRoleRepository,
)
from ...dependencies import (
    check_active,
    check_block,
    generate_jwt,
    validate_session_add,
    validate_update_session,
)
from ...services import check_users_sessions
from ...services.encode_decode_get_put_jwt_data_auth import (
    put_jwt_data_auth_cookie,
)
from ..check_user_sessions import check_ban_until


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo_user = UserRepository(session)
        self.repo_role = RoleRepository(session)
        self.repo_user_role = UserRoleRepository(session)
        self.repo_session = SessionRepository(session)
        self.session = session

    async def add_auth_data(
        self,
        request: Request,
        user_id: UUID,
        user_name: str,
        response: Response,
    ):
        check_user_session = await self.repo_session.get_filter(
            ip=request.client.host,
            user_agent=request.headers.get("user-agent"),
            user_id=user_id,
        )
        if not check_user_session:
            user_session = await validate_session_add(
                session=self.session, request=request, user_id=user_id
            )

        else:
            user_session = await validate_update_session(
                session=self.session,
                request=request,
                auth_public_uid=check_user_session[0].id,
            )

        access_token = generate_jwt(
            auth_ssid=user_session.auth_ssid, user_id=user_id.hex, user_name=user_name
        )

        put_jwt_data_auth_cookie(
            access_token=access_token,
            auth_public_uid=user_session.id,
            auth_ssid=user_session.auth_ssid,
            auth_refresh_token=user_session.refresh_token,
            response=response,
        )

        return access_token, user_session

    async def check_auth_email_user(self, nickname: str, user_email: str) -> Any:
        user = await self.repo_user.get_filter(email=user_email)

        if not user:
            user_add = await self.repo_user.add(email=user_email, nickname=nickname)

            role = await self.repo_role.get_filter(name="user")
            print(role[0].id)
            await self.repo_user_role.add(user_id=user_add.id, role_id=role[0].id)

            return user_add

        await check_active(session=self.session, user_id=user[0].id)
        await check_ban_until(session=self.session, user_id=user[0].id)
        await check_block(session=self.session, user_id=user[0].id)

        return user[0]

    async def check_update_auth_data(
        self,
        request: Request,
        response: Response,
        auth_data: dict[str, str],
    ) -> Any:
        from src.dependencies.generate import generate_jwt
        from src.dependencies.validation import (
            validate_session_get_id,
            validate_update_session,
            validate_user_get_id,
        )

        user_session = await validate_session_get_id(
            session=self.session, session_id=auth_data["auth_public_uid"]
        )

        await check_users_sessions(
            session=self.session,
            request=request,
            refresh_token=True,
            user_id_from_session=user_session.user_id,
        )
        session_upd = await validate_update_session(
            session=self.session,
            request=request,
            auth_public_uid=auth_data["auth_public_uid"],
        )

        user_data = await validate_user_get_id(
            session=self.session, user_id=session_upd.user_id
        )

        access_token = generate_jwt(
            user_id=user_data.id.hex,
            auth_ssid=session_upd.auth_ssid,
            user_name=user_data.name,
        )

        put_jwt_data_auth_cookie(
            response=response,
            auth_ssid=session_upd.auth_ssid,
            auth_refresh_token=session_upd.refresh_token,
            access_token=access_token,
            auth_public_uid=session_upd.id,
        )

        return access_token, user_data, session_upd
