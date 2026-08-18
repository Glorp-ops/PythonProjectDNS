from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.check_user_sessions import check_users_sessions
from src.services.encode_decode_get_put_jwt_data_auth.get_put_jwt_data_auth_cookie import (
    delete_auth_data,
)

from ..database.sqlalchemy_connect import get_session
from ..dependencies import (
    validate_delete_session,
    validate_delete_session_with_and,
    validate_user_delete,
)

router = APIRouter(prefix="/api/v1/live", tags=["exit-delete-profile"])


@router.delete("/logout")
async def logout(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
    response: Response,
):

    payload_validate, auth_data = await check_users_sessions(
        session=session, request=request, permission="profile:logout"
    )

    delete_auth_data(response=response, auth_data=auth_data)

    await validate_delete_session_with_and(
        session=session,
        user_id=payload_validate.userId,
        auth_public_uid=auth_data["auth_public_uid"],
    )

    return {"result": True}


@router.delete("/profile")
async def delete_profile(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    response: Response,
):

    payload_validate, auth_data = await check_users_sessions(
        session=session,
        request=request,
        permission="profile:delete_own",
    )

    await validate_delete_session(session=session, user_id=payload_validate.userId)
    await validate_user_delete(session=session, user_id=payload_validate.userId)

    print(payload_validate.userId)

    delete_auth_data(response=response, auth_data=auth_data)

    return {"result": True}
