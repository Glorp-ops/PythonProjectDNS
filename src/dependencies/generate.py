from random import choices
from secrets import randbelow
from string import ascii_uppercase, digits
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ..services.encode_decode_get_put_jwt_data_auth import (
    encode_jwt,
)
from .validation import validate_user_nickname


def generate_jwt(user_id: str, auth_ssid: str, user_name: str | None):

    payload = {
        "authSSID": auth_ssid,
        "jti": uuid4().hex,
        "userId": user_id,
        "userName": user_name,
    }

    access_token = encode_jwt(payload=payload)

    return access_token


async def generate_nickname(session: AsyncSession) -> str:
    while True:
        prefix = "Пришелец-"
        words = choices(ascii_uppercase, k=4)
        numbers = choices(digits, k=7)
        nickname = prefix + "".join(words) + "".join(numbers)

        if not await validate_user_nickname(session=session, nickname=nickname):
            return nickname


def random_code():
    return str(randbelow(9_999_999) + 1_000_000)


def build_tree(categories):
    node_map = {}

    for c in categories:
        node_map[c.id] = {"id": c.id, "name": c.name, "slug": c.slug, "children": []}

    root = []

    for c in categories:
        if c.parent_id is None:
            root.append(node_map[c.id])
        else:
            node_map[c.parent_id]["children"].append(node_map[c.id])

    return root
