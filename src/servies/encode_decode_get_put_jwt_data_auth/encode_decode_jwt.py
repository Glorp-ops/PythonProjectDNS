from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any

import jwt
from src.core.config import settings


async def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.settings_jwt.PRIVATE_KEY.read_text(),
    expires_in: int = settings.settings_jwt.EXPIRATION_ACCESS,
    timedelta_expires: timedelta | None = None,
    algorithm: str = settings.settings_jwt.ALGORITHM,
):
    payload_encoded = payload.copy()
    now = datetime.now(UTC)

    if timedelta_expires:
        payload_encoded["exp"] = int((now + timedelta_expires).timestamp())

    else:
        payload_encoded["exp"] = int((now + timedelta(seconds=expires_in)).timestamp())

    payload_encoded["iat"] = int(now.timestamp())

    payload_encoded["rnd"] = ""

    return jwt.encode(payload_encoded, private_key, algorithm=algorithm)


async def decode_jwt(
    token: str,
    public_key: str = settings.settings_jwt.PUBLIC_KEY.read_text(),
    algorithm: str = settings.settings_jwt.ALGORITHM,
):

    return jwt.decode(jwt=token, key=public_key, algorithm=[algorithm])


async def hask_jwt(token: str):
    return sha256(token.encode()).hexdigest()
