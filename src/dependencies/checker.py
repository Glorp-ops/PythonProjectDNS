from datetime import UTC, datetime
from uuid import UUID

from bcrypt import checkpw
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..database.repositories_db import (
    ProductsRepository,
    SessionRepository,
    UserRepository,
)
from .validation import validate_user_get_id


async def check_block(session: AsyncSession, user_id: UUID):

    user = await validate_user_get_id(session=session, user_id=user_id)

    if user.is_blocked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User blocked")


async def check_active(session: AsyncSession, user_id: UUID):

    user = await validate_user_get_id(session=session, user_id=user_id)

    if not user.active_at:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not active")


async def check_revoked(session: AsyncSession, auth_public_uid: str):

    try:
        user_session = await SessionRepository(session).get_filter(id=auth_public_uid)
        revoke = user_session[0].revoked

    except IndexError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        ) from e

    if revoke:
        await SessionRepository(session).delete(id=auth_public_uid)

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session revoked")


async def check_exp_sessions(session: AsyncSession, auth_public_uid: str):

    user_session = await SessionRepository(session=session).get_filter(id=auth_public_uid)

    if user_session[0].expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")


async def verify_password_to_id(session: AsyncSession, user_id: UUID, password: str):
    user = await validate_user_get_id(session=session, user_id=user_id)

    if checkpw(password.encode(), bytes.fromhex(user.password)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have such the password",
        )

    return user


async def verify_password_to_email(session: AsyncSession, email: str, password: str):

    user = await UserRepository(session).get_filter(email=email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not checkpw(password.encode(), bytes.fromhex(user[0].password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="error password or email",
        )

    return user[0]


async def check_products(product_id: int, session: AsyncSession, quantity: int | None = None):
    print(product_id)

    product = await ProductsRepository(session).get_filter(id=product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    print(product[0].quantity)
    print(product[0].is_deleted)
    print(product[0].active_at)

    if (
        (product[0].quantity <= (quantity or 1))
        or product[0].is_deleted
        or not product[0].active_at
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This item is unavailable",
        )

    return product
