from asyncio import gather
from typing import Annotated
from uuid import uuid4

from bcrypt import gensalt, hashpw
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Request,
    Response,
)
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.repositories_db import SessionRepository
from ..database.sqlalchemy_connect import get_session
from ..dependencies import (
    random_code,
    validate_get_auth_step_token,
    validate_update_user,
    verify_password_to_id,
)
from ..redis_db import repo_auth_email
from ..schemes import AuthEmail, EmailInfo, TokenInfo, UpdatePassword, UpdatePasswordCode
from ..services import check_users_sessions, send_email, validate_code
from ..services.encode_decode_get_put_jwt_data_auth import (
    delete_auth_step_token,
    put_auth_step_token,
)
from ..services.services_layer import AuthService

router = APIRouter(prefix="/api/v1/update-password", tags=["update-password"])


@router.post("/password", status_code=201)
async def update_password(
    user_password: UpdatePassword,
    background_tasks: BackgroundTasks,
    request: Request,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    payload_validate, _ = await check_users_sessions(
        session=session,
        request=request,
        permission="profile:update_password",
    )

    user = await verify_password_to_id(
        session=session,
        password=user_password.password,
        user_id=payload_validate.userId,
    )

    email = AuthEmail(recipients=[user.email])
    code = random_code()
    secret = uuid4().hex

    await repo_auth_email.set_data_auth(
        email=email.recipients[0].email,
        secret=secret,
        code=code,
        password=hashpw(user_password.password.encode("utf-8"), gensalt()).hex(),
    )

    put_auth_step_token(response=response, secret=secret)

    background_tasks.add_task(send_email, email.recipients, code)

    return {"data": EmailInfo()}


@router.patch("/code")
async def check_code(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_code: UpdatePasswordCode,
    response: Response,
    request: Request,
):

    payload_validate, auth_data = await check_users_sessions(session=session, request=request)

    secret = validate_get_auth_step_token(request=request)
    email = await repo_auth_email.manager.redis.get(f"auth:{secret}")

    code, password = await gather(
        repo_auth_email.manager.redis.get(f"auth:code:{email}"),
        repo_auth_email.manager.redis.get(f"auth:password:{email}"),
    )

    await validate_code(email, code, user_code=user_code.code, secret=secret)

    user_upd = await validate_update_user(
        session=session,
        user_id=payload_validate.userId,
        values={"password": password},
    )

    access_token, _, session_data = await AuthService(session).check_update_auth_data(
        request=request, response=response, auth_data=auth_data
    )

    await SessionRepository(session).delete_all_sessions_except_current(
        user_id=user_upd.id, auth_public_uid=session_data.id
    )
    await repo_auth_email.delete_auth_data(secret=secret, email=email[0], password=True)
    delete_auth_step_token(response=response, secret=secret)

    return {
        "data": TokenInfo(access_token=access_token, refresh_token=session_data.refresh_token),
        "user": {"id": user_upd.id, "email": user_upd.email},
    }
