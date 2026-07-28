from fastapi import Request, Response

from ...core import settings


def get_jwt_data_auth_cookie(request: Request):

    auth_access_token = request.cookies.get("access_token")
    auth_public_uid = request.cookies.get("auth_public_uid")
    auth_refresh_token = request.cookies.get("auth_refresh_token")
    auth_ssid = request.cookies.get("auth_ssid")

    return {
        "access_token": auth_access_token,
        "auth_public_uid": auth_public_uid,
        "auth_refresh_token": auth_refresh_token,
        "auth_ssid": auth_ssid,
    }


def put_jwt_data_auth_cookie(
    access_token: str,
    auth_public_uid: str,
    auth_refresh_token: str,
    auth_ssid: str,
    response: Response,
    expires_jwt: int = settings.settings_jwt.EXPIRATION_ACCESS,
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
    response.set_cookie(
        "auth_public_uid",
        expires=expires_session,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_public_uid,
    )
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


def put_auth_step_token(response: Response, secret: str):

    response.set_cookie(
        "auth_step_token",
        expires=300,
        secure=True,
        httponly=True,
        samesite="lax",
        value=secret,
    )


def get_auth_step_token(reauest: Request):
    return reauest.cookies.get("auth_step_token")


def delete_auth_step_token(response: Response, secret: str):
    response.set_cookie(
        "auth_step_token",
        expires=0,
        secure=True,
        httponly=True,
        samesite="lax",
        value=secret,
    )


def delete_auth_data(response: Response, auth_data: dict[str, str]):
    response.set_cookie(
        "access_token",
        expires=0,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_data["access_token"],
    )
    response.set_cookie(
        "auth_public_uid",
        expires=0,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_data["auth_public_uid"],
    )
    response.set_cookie(
        "auth_refresh_token",
        expires=0,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_data["auth_refresh_token"],
    )
    response.set_cookie(
        "auth_ssid",
        expires=0,
        secure=True,
        httponly=True,
        samesite="lax",
        value=auth_data["auth_ssid"],
    )
