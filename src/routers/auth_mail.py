from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Request, Response
from fastapi.background import BackgroundTasks
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.sqlalchemy_connect import get_session
from ..dependencies import (
    random_code,
    validate_get_auth_step_token,
    validate_user_email_with_nickname,
)
from ..redis_db import repo_auth_email
from ..schemes import AuthEmail, CheckCode, EmailInfo, TokenInfo
from ..services import send_email, validate_code
from ..services.encode_decode_get_put_jwt_data_auth import (
    delete_auth_step_token,
    put_auth_step_token,
)
from ..services.services_layer import AuthService

router = APIRouter(prefix="/api/v1/auth-mail", tags=["auth-mail"])


@router.post("/email", status_code=201)
async def auth_mail(mail: AuthEmail, background_tasks: BackgroundTasks, response: Response):

    secret = uuid4().hex
    code = random_code()
    await repo_auth_email.set_data_auth(
        email=mail.recipients[0].email, code=code, secret=secret
    )
    background_tasks.add_task(send_email, mail.recipients, code)
    put_auth_step_token(response=response, secret=secret)

    return {"data": EmailInfo()}


@router.post("/code", status_code=201)
async def user_check_code(
    user_code: CheckCode,
    request: Request,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    secret = validate_get_auth_step_token(request=request)

    email = await repo_auth_email.manager.redis.get(f"auth:{secret}")
    code = await repo_auth_email.manager.redis.get(f"auth:code:{email}")

    await validate_code(email, code, user_code=user_code.code, secret=secret)
    user = await validate_user_email_with_nickname(
        email=email, session=session, request=request
    )

    access_token, user_session = await AuthService(session).add_auth_data(
        request=request, user_id=user.id, user_name=user.name, response=response
    )

    await repo_auth_email.delete_auth_data(secret=secret, email=email[0])
    delete_auth_step_token(response=response, secret=secret)

    return {
        "data": TokenInfo(access_token=access_token, refresh_token=user_session.refresh_token),
        "user": {"id": user.id, "email": user.email},
    }
