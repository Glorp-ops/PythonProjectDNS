from bcrypt import checkpw
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from ..core import settings
from ..database.repositories_db import UserRepository
from ..database.sqlalchemy_connect import async_session
from ..dependencies import check_active, check_block
from ..services import check_role_permission


class AuthAdmin(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with async_session() as session:
            user = await UserRepository(session).get_filter(nickname=username)
            await check_active(session, user[0].id)
            await check_block(session, user[0].id)

            if not user:
                return False

            if not checkpw(password.encode(), bytes.fromhex(user[0].password)):
                return False

            role_data = await check_role_permission(
                session=session, user_id=user[0].id, permission="admin:panel"
            )

            request.session.update(
                {"user_id": user[0].id.hex, "role": [role.name for role in role_data]}
            )

            return True

    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        user_id = request.session.get("user_id")
        if not request.session.get("user_id") or not user_id:
            return False

        return True


authentication_backend = AuthAdmin(secret_key=settings.AUTH_ADMIN_KEY)
