from fastapi import Cookie, Response

from src.core.config import settings


async def get_jwt_data_auth_cookie(cookie=Cookie()):
    auth_access_token = cookie.get("access_token")
    auth_public_uid = cookie.get("auth_public_uid")
    auth_refresh_token = cookie.get("auth_refresh_token")
    auth_ssid = cookie.get("auth_ssid")

    return {
        "access_token": auth_access_token,
        "auth_public_uid": auth_public_uid,
        "auth_refresh_token": auth_refresh_token,
        "auth_ssid": auth_ssid,
    }


async def put_jwt_data_auth_cookie(
    access_token: str,
    expires_jwt: int,
    # public_uid: str,
    auth_refresh_token: str,
    auth_ssid: str,
    response: Response,
    expires_session: int = settings.settings_jwt.EXPIRATION_SESSION,
):
    response.set_cookie(
        "access_token",
        expires=expires_jwt,
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=856,
        value=access_token,
    )
    # response.set_cookie(
    #     "auth_public_uid",
    #     expires=expires_session,
    #     secure=True,
    #     httponly=True,
    #     samesite="lax",
    #     value=public_uid,
    # )
    response.set_cookie(
        "auth_refresh_token",
        expires=expires_session,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_refresh_token,
    )
    response.set_cookie(
        "auth_ssid",
        expires=expires_session,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_ssid,
    )

    return response
