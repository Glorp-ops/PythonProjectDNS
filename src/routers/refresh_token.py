from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.sqlalchemy_connect import get_session
from ..services.encode_decode_get_put_jwt_data_auth import (
    get_jwt_data_auth_cookie,
)
from ..services.services_layer import AuthService

router = APIRouter(prefix="/api/v1/refresh-token", tags=["refresh-token"])


@router.post("", status_code=201)
async def refresh_token(
    request: Request,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    auth_data = get_jwt_data_auth_cookie(request=request)
    print(auth_data["auth_public_uid"])

    access_token, _ = await AuthService(session).check_refresh_auth_data(
        request=request, response=response, auth_data=auth_data
    )

    return {"access_token": access_token}
