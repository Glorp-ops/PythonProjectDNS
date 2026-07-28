from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.sqlalchemy_connect import get_session
from ..dependencies import check_active, check_block, verify_password_to_email
from ..schemes import AuthEmailWithPassword, TokenInfo
from ..services.services_layer import AuthService

router = APIRouter(
    prefix="/api/v1/auth-email-with-password", tags=["auth-email-with-password"]
)


@router.post("", status_code=201)
async def auth_email_with_password(
    session: Annotated[AsyncSession, Depends(get_session)],
    credentials: AuthEmailWithPassword,
    request: Request,
    response: Response,
):

    user = await verify_password_to_email(
        session=session, password=credentials.password, email=credentials.email
    )

    await check_active(session=session, user_id=user.id)
    await check_block(session=session, user_id=user.id)

    access_token, user_session = await AuthService(session).add_auth_data(
        request=request, user_id=user.id, user_name=user.name, response=response
    )

    return {
        "data": TokenInfo(access_token=access_token, refresh_token=user_session.refresh_token),
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }
