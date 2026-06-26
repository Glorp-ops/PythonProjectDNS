from fastapi import Header, Request, Response


async def put_jwt_data_auth_headers(
    access_token: str, refresh_token: str, response: Response, auth_ssid: str
):

    response.headers["set-cookie"] = "auth_access_token=" + access_token
    response.headers["set-cookie"] = "auth_refresh_token=" + refresh_token
    response.headers["set-cookie"] = "auth_ssid=" + auth_ssid


async def get_jwt_data_auth_headers(header=Header(alias="set-cookie")):
    return header


async def get_user_agent(request: Request):

    return request.headers.get("User-Agent")
