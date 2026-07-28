from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.sqlalchemy_connect import get_session
from ..dependencies import (
    validate_user_get_id,
)
from ..schemes import UserData
from ..services import check_users_sessions, validate_check_edit_user_settings

router = APIRouter(prefix="/api/v1/user-settings", tags=["user-settings"])


@router.get("")
async def get_user_data(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    payload_validate, _ = await check_users_sessions(
        session=session, request=request, permission="profile:view_own"
    )

    user = await validate_user_get_id(user_id=payload_validate.userId, session=session)

    return {
        "data": {
            "name": user.name,
            "nickname": user.nickname,
            "surname": user.surname,
            "email": user.email,
        }
    }


@router.patch("")
async def edit_user_data(
    user_data: UserData,
    response: Response,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
):

    payload_validate, auth_data = await check_users_sessions(
        session=session, request=request, permission="profile:edit_own"
    )

    user_upd = await validate_check_edit_user_settings(
        session=session,
        user_id=payload_validate.userId,
        user_data=user_data,
        auth_data=auth_data,
        request=request,
        response=response,
    )

    return {
        "data": {
            "id": user_upd.id,
            "name": user_upd.name,
            "surname": user_upd.surname,
            "nickname": user_upd.nickname,
            "email": user_upd.email,
        }
    }
