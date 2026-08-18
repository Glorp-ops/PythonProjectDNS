from uuid import UUID

from fastapi import HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..core import settings
from ..schemes import UserData
from ..services.encode_decode_get_put_jwt_data_auth import (
    put_jwt_data_auth_cookie,
)


async def validate_check_edit_user_settings(
    session: AsyncSession,
    user_id: UUID,
    user_data: UserData,
    auth_data: dict[str, str],
    response: Response,
    request: Request,
):
    from ..dependencies import (
        generate_jwt,
        validate_delete_session_with_and_not,
        validate_update_session,
        validate_update_user,
        validate_user_email_with_and_not,
        validate_user_get_id,
        validate_user_nickname_with_and_not,
    )

    user_data_dict = user_data.model_dump()

    if not user_data_dict["email"]:
        user_data_dict.pop("email")

    else:
        await validate_user_email_with_and_not(session, email=user_data.email, user_id=user_id)

    if not user_data_dict["nickname"]:
        user_data_dict.pop("nickname")

    else:
        await validate_user_nickname_with_and_not(
            session, nickname=user_data.nickname, user_id=user_id
        )

    print(user_data_dict)
    user = await validate_user_get_id(session=session, user_id=user_id)

    for key in list(user_data_dict):
        value = user_data_dict[key]

        if value in [
            user.name,
            user.nickname,
            user.email,
            user.surname,
        ]:
            del user_data_dict[key]

    print(user_data_dict)

    if user_data_dict == {}:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="user did not change anything"
        )

    if ("email" not in user_data_dict) and ("nickname" not in user_data_dict):
        user_upd = await validate_update_user(
            session=session, user_id=user_id, values=user_data_dict
        )
        access_token = generate_jwt(
            user_id=user_id.hex,
            auth_ssid=auth_data["auth_ssid"],
            user_name=user_data_dict.get("name"),
        )
        response.set_cookie(
            "access_token",
            expires=settings.settings_jwt.EXPIRATION_ACCESS,
            secure=True,
            httponly=True,
            samesite="lax",
            max_age=856,
            value=access_token,
        )

        return user_upd

    else:
        access_token = generate_jwt(
            user_id=user_id.hex,
            auth_ssid=auth_data["auth_ssid"],
            user_name=user_data.name,
        )

        user_upd = await validate_update_user(
            session=session, user_id=user_id, values=user_data_dict
        )

        session_upd = await validate_update_session(
            session=session,
            request=request,
            auth_public_uid=auth_data["auth_public_uid"],
        )

        await validate_delete_session_with_and_not(
            session=session,
            user_id=user_id,
            auth_public_uid=session_upd.id,
        )

        put_jwt_data_auth_cookie(
            response=response,
            auth_ssid=session_upd.auth_ssid,
            auth_refresh_token=session_upd.refresh_token,
            access_token=access_token,
            auth_public_uid=session_upd.id,
        )

        return user_upd
