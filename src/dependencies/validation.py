import datetime
from hashlib import sha256
from secrets import token_urlsafe
from typing import Any
from uuid import UUID

from fastapi import HTTPException, Request, status
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from jwt import InvalidTokenError

from ..core import settings
from ..database.repositories_db import (
    LikeRepository,
    ProductsRepository,
    SessionRepository,
    UserRepository,
    FavoriteRepository,
)
from ..redis_db import repo_auth_email
from ..schemes import AccessTokenPayload
from ..services.encode_decode_get_put_jwt_data_auth import decode_jwt, get_auth_step_token


async def validate_delete_session(session: AsyncSession, user_id: UUID):
    session_data = await SessionRepository(session).delete(user_id=user_id)

    if not session_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")


def validate_email(
    key: list[str],
):
    print(key)
    try:
        email: str = key[0].replace("<", ":").replace(">", ":").split(":")[2]
    except IndexError as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Your email verification code has expired. Request a new code.",
        ) from e
    return email


def validate_payload(token: str | bytes) -> AccessTokenPayload:
    try:
        payload_validate = AccessTokenPayload.model_validate(decode_jwt(token=token))
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid access token"
        ) from e

    return payload_validate


async def validate_check_session(
    session: AsyncSession, auth_public_uid: str, refresh_token: str, auth_ssid: str
):
    session_db = await SessionRepository(session).get_filter(id=auth_public_uid)

    if session_db[0].auth_ssid != auth_ssid and session_db[0].refresh_token != refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")


async def validate_update_session(
    session: AsyncSession, request: Request, auth_public_uid: str
):
    try:
        session_upd = await SessionRepository(session).update(
            model_id=auth_public_uid,
            id=token_urlsafe(16),
            auth_ssid=sha256(token_urlsafe(32).encode()).hexdigest(),
            refresh_token=sha256(token_urlsafe(32).encode()).hexdigest(),
            user_agent=request.headers.get("user-agent"),
            ip=request.client.host,
            expires_at=settings.settings_jwt.EXPIRATION_SESSION,
            created_at=datetime.datetime.now(tz=datetime.UTC),
            update=True,
        )

        return session_upd

    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Don't found session "
        ) from e


async def validate_user_get_id(user_id: UUID, session: AsyncSession):

    user_data = await UserRepository(session).get_id(user_id)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_data


async def validate_user_email_with_nickname(
    email: str, session: AsyncSession, request: Request
):
    from src.dependencies.generate import generate_nickname
    from src.services.services_layer.auth_services import AuthService

    try:
        user = await AuthService(session).check_auth_emai_user(
            email_user=email,
            nickname=await generate_nickname(session=session),
            request=request,
        )
    except ConnectionRefusedError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable. Please try again later.",
        ) from e

    return user


async def validate_user_nickname(session: AsyncSession, nickname: str):
    users_nickname = await UserRepository(session).get_filter(nickname=nickname)

    if users_nickname:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error validation")

    return users_nickname


async def validate_user_nickname_with_and_not(
    session: AsyncSession, nickname: str, user_id: UUID
):
    users_nickname = await UserRepository(session).get_filter_with_and_not(
        nickname=nickname, model_id=user_id
    )

    if users_nickname:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error validation")

    return users_nickname


async def validate_update_user_email(
    session: AsyncSession, email: str, values: dict[str, Any]
):

    user_upd = await session.scalar(
        update(UserRepository.model)
        .values(**values)
        .where(UserRepository.model.email == email)
        .returning(UserRepository.model)
    )
    if not user_upd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await session.commit()

    return user_upd


async def validate_update_user(session: AsyncSession, user_id: UUID, values: dict[str, Any]):

    user_upd = await UserRepository(session).update(user_id, **values)

    if not user_upd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user_upd


async def validate_delete_session_with_and_not(
    session: AsyncSession, user_id: UUID, auth_public_uid: str
):
    print(auth_public_uid)

    user_session = await SessionRepository(session).delete_with_and_not(
        user_id=user_id, auth_public_uid=auth_public_uid
    )

    if not user_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return user_session


async def validate_session_get_id(session: AsyncSession, session_id: str):
    try:
        user_session = await SessionRepository(session).get_id(id=session_id)

    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        ) from e

    if not user_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    return user_session


def validate_get_auth_step_token(request: Request):
    secret = get_auth_step_token(reauest=request)

    if not secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    return secret


async def validate_get_redis(key: str):
    value = await repo_auth_email.manager.redis.get(key)

    if not value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="value not found")


async def validate_user_email_with_and_not(session: AsyncSession, email: str, user_id: UUID):
    users_email = await UserRepository(session).get_filter_with_and_not(
        email=email, model_id=user_id
    )

    if users_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error validation")

    return users_email


async def validate_delete_session_with_and(
    session: AsyncSession, user_id: UUID, auth_public_uid: str
):
    user_session = await SessionRepository(session).delete_with_and(
        user_id=user_id, auth_public_uid=auth_public_uid
    )

    if not user_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    return user_session


async def validate_user_delete(session: AsyncSession, user_id: UUID):
    user = await UserRepository(session).delete(id=user_id)

    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


async def validate_session_add(session: AsyncSession, request: Request, user_id: UUID):

    user_session = await SessionRepository(session).add(
        user_agent=request.headers.get("user-agent"),
        ip=request.client.host,
        user_id=user_id,
    )
    if not user_session:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user_session


async def validate_product_get_id_with_join_and_description(
    session: AsyncSession, product_id: int
):

    try:
        product = await ProductsRepository(session).get_id_with_join_and_description(
            product_id=product_id
        )

    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from e

    return product


async def validate_create_like_review(session: AsyncSession, user_id: UUID, review_id):
    try:
        like_data, like_count = await LikeRepository(session).create_review_like(
            review_id=review_id, user_id=user_id
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="There's already a like"
        ) from e

    return like_data, like_count


async def validate_add_favorites(session: AsyncSession, user_id: UUID, product_id: int):
    try:
        favorite = await FavoriteRepository(session).add(
            product_id=product_id, user_id=user_id
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user has this product in their favorites.",
        )

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Don't found product_id",
        )

    return favorite
