from asyncio import gather
from typing import Annotated
from uuid import uuid4

from bcrypt import gensalt, hashpw
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from ..database.repositories_db import UserRepository
from ..database.sqlalchemy_connect import get_session
from ..dependencies import (
    random_code,
    validate_get_auth_step_token,
    validate_update_user_email,
)
from ..redis_db import repo_auth_email
from ..schemes import AuthEmail, EmailInfo, UpdatePassword, UpdatePasswordCode
from ..services import send_email, validate_code
from ..services.encode_decode_get_put_jwt_data_auth import (
    put_auth_step_token,
)

router = APIRouter(prefix="/api/v1/forgot-password", tags=["forgot_password"])


@router.post("/email", status_code=201)
async def write_email(
    session: Annotated[AsyncSession, Depends(get_session)],
    email: AuthEmail,
    response: Response,
):
    secret = uuid4().hex
    put_auth_step_token(response=response, secret=secret)

    await repo_auth_email.manager.set(
        key=f"auth:{secret}", value=email.recipients[0].email, ex=300
    )

    user_data = await UserRepository(session).check_user_email(email.recipients[0].email)

    return {"status": "success", "user_data": user_data}


@router.post("/password", status_code=201)
async def update_password(
    user_password: UpdatePassword,
    background_tasks: BackgroundTasks,
    request: Request,
):

    code = random_code()
    secret = validate_get_auth_step_token(request=request)
    email = await repo_auth_email.manager.get(f"auth:{secret}")

    await repo_auth_email.set_data_auth(
        email=email,
        secret=secret,
        code=code,
        password=hashpw(user_password.password.encode("utf-8"), gensalt()).hex(),
    )

    background_tasks.add_task(send_email, [email], code)

    return {"data": EmailInfo()}


@router.patch("/code")
async def check_code(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_code: UpdatePasswordCode,
    request: Request,
):

    secret = validate_get_auth_step_token(request=request)
    email = await repo_auth_email.manager.redis.get(f"auth:{secret}")

    code, password = await gather(
        repo_auth_email.manager.redis.get(f"auth:code:{email}"),
        repo_auth_email.manager.redis.get(f"auth:password:{email}"),
    )

    await validate_code(email, code, user_code=user_code.code, secret=secret)

    user_upd = await validate_update_user_email(
        session=session,
        email=email,
        values={"password": password},
    )

    return {
        "status": "success",
        "user": {"id": user_upd.id, "email": user_upd.email},
    }
