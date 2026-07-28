from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any

import jwt

from ...core import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.settings_jwt.PRIVATE_KEY.read_text(),
    expires_in: int = settings.settings_jwt.EXPIRATION_ACCESS,
    algorithm: str = settings.settings_jwt.ALGORITHM,
):
    payload_encoded = payload.copy()
    now = datetime.now(UTC)

    payload_encoded["exp"] = int((now + timedelta(seconds=expires_in)).timestamp())

    payload_encoded["iat"] = int(now.timestamp())

    payload_encoded["rnd"] = ""

    return jwt.encode(payload_encoded, private_key, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.settings_jwt.PUBLIC_KEY.read_text(),
    algorithm: str = settings.settings_jwt.ALGORITHM,
):

    return jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])


def hask_jwt(token: str):
    return sha256(token.encode()).hexdigest()
