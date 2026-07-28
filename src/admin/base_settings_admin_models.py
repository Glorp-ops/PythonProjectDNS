from fastapi import HTTPException
from sqladmin import ModelView
from starlette import status
from starlette.requests import Request

from ..database.sqlalchemy_connect import async_session
from ..dependencies import check_active, check_block
from ..services import check_role_permission


class BaseAdminSettings(ModelView):
    form_include_pk = True
    _permission: str = ""

    async def is_accessible(self, request: Request) -> bool:
        user_id = request.session.get("user_id")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not request.session.get("role"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        async with async_session() as session:
            await check_block(session, user_id)
            await check_active(session, user_id)
            if not await check_role_permission(
                session, user_id, permission=self._permission, for_admin=True
            ):
                return False

        return True
