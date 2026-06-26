import datetime
import logging
from hashlib import sha256
from secrets import token_urlsafe
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.background import BackgroundTasks
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.config import settings
from src.database.repositories_db.session_repository import SessionRepository
from src.database.repositories_db.user_repository import UserRepository
from src.database.sqlalchemy_connect.connect_db import get_session
from src.dependencies.generate_nickname import generate_nickname
from src.redis_db.repositories_redis.redis_auth_email import repo_auth_email
from src.schemes.auth_email import AuthEmail
from src.schemes.check_code import CheckCode
from src.schemes.email_info import EmailInfo
from src.servies.encode_decode_get_put_jwt_data_auth.encode_decode_jwt import encode_jwt
from src.servies.encode_decode_get_put_jwt_data_auth.get_put_jwt_data_auth_cookie import (
    put_jwt_data_auth_cookie,
)
from src.servies.encode_decode_get_put_jwt_data_auth.get_put_jwt_data_auth_headers import (
    get_user_agent,
    put_jwt_data_auth_headers,
)
from src.servies.send_validate_mail import random_code, send_email, validate_code

router = APIRouter(prefix="/auth_mail", tags=["auth_mail"])


@router.post("/send_mail")
async def auth_mail(mail: AuthEmail, background_tasks: BackgroundTasks):
    code = await random_code()
    await repo_auth_email.set_data_auth(email=mail.recipients[0], code=code)
    background_tasks.add_task(send_email, mail.recipients, code)

    return {"data": EmailInfo()}


@router.post("/user_code")
async def user_check_code(
    user_code: CheckCode,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
):

    exp_session = settings.settings_jwt.EXPIRATION_SESSION
    key = await repo_auth_email.manager.redis.keys(
        "auth:litemike134 <litemike134@gmail.com>:attempts:"
    )
    try:
        email: str = key[0].replace("<", ":").replace(">", ":").split(":")[2]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Your email verification code has expired. Request a new code.",
        )

    logging.info(email)

    code = await repo_auth_email.manager.redis.get(
        "auth:code:litemike134 <litemike134@gmail.com>"
    )

    logging.info(code)
    logging.info(user_code.code)

    await validate_code(email, code, user_code=user_code.code)

    user = await UserRepository(session).check_auth_emai_user(
        nickname=await generate_nickname(), email=email
    )

    logging.info(user)
    user_session = await SessionRepository(session).add(
        auth_ssid=sha256(token_urlsafe(32).encode()).hexdigest(),
        refresh_token=sha256(token_urlsafe(32).encode()).hexdigest(),
        user_agent=await get_user_agent(request),
        auth_public_uid=token_urlsafe(16),
        ip=request.client.host,
        expires_at=exp_session,
        created_at=datetime.datetime.now(tz=datetime.UTC),
        user_id=[data.id for data in user][0],
    )
    auth_ssid = [session.auth_ssid for session in user_session][0]
    refresh_token = [data.refresh_token for data in user_session][0]

    payload = {
        "authSSID": auth_ssid,
        "jti": uuid4().hex,
        "userId": [data.id for data in user][0].hex,
        "userName": [data.name for data in user][0],
    }

    access_token = await encode_jwt(payload=payload)

    await put_jwt_data_auth_cookie(
        access_token=access_token,
        expires_jwt=settings.settings_jwt.EXPIRATION_ACCESS,
        expires_session=exp_session,
        auth_ssid=auth_ssid,
        auth_refresh_token=refresh_token,
        response=response,
    )

    return {"message": "success"}
