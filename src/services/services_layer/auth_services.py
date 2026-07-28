from typing import Any
from uuid import UUID

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..check_user_sessions import check_ban_until
from ...database.repositories_db import (
    RoleRepository,
    UserRepository,
    UserRoleRepository,
)
from ...dependencies import generate_jwt, validate_session_add, check_active, check_block
from ...services import check_users_sessions
from ...services.encode_decode_get_put_jwt_data_auth import (
    put_jwt_data_auth_cookie,
)


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo_user = UserRepository(session)
        self.repo_role = RoleRepository(session)
        self.repo_user_role = UserRoleRepository(session)
        self.session = session

    async def add_auth_data(
        self, request: Request, user_id: UUID, user_name: str, response: Response
    ):

        user_session = await validate_session_add(
            session=self.session, request=request, user_id=user_id
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

    async def check_auth_emai_user(
        self, nickname: str, email_user: str, request: Request
    ) -> Any:
        user = await self.repo_user.get_filter(email=email_user)

        if not user:

            user_add = await self.repo_user.add(email=email_user, nickname=nickname)

            role = await self.repo_role.get_filter(name="user")

            await self.repo_user_role.add(user_id=user_add.id, role_id=role[0].id)

            return user_add

        await check_active(session=self.session, user_id=user[0].id)
        await check_ban_until(session=self.session, user_id=user[0].id)
        await check_block(session=self.session, user_id=user[0].id)

        return user[0]

    async def check_refresh_auth_data(
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

        return access_token, user_data
