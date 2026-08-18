from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..database.repositories_db import FavoriteRepository
from ..database.sqlalchemy_connect import get_session
from ..dependencies.validation import validate_add_favorites
from ..schemes import CartItem, pagination
from ..services import check_users_sessions
from ..services.services_layer import FavoriteServices

router = APIRouter(prefix="/api/v1/favorites", tags=["favorite"])


@router.post("", status_code=201)
async def create_favorite(
    product: CartItem,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="favorites:create"
    )
    favorite = await validate_add_favorites(
        session, payload_validate.userId, product.product_id
    )

    return {"status": "success", "favorite": favorite}


@router.get("")
async def get_favorites(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    pagination: pagination,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="favorites:view"
    )

    favorite_data, total_count, pagination_settings = await FavoriteServices(
        session
    ).get_favorites(
        user_id=payload_validate.userId, page=pagination.page, size=pagination.size
    )

    return {
        "status": "success",
        "total_count": total_count,
        "favorites_data": favorite_data,
        "pagination": pagination_settings,
    }


@router.get("/{product_id}")
async def get_favorite(
    product_id: Annotated[int, Path(gt=0)],
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="favorites:view"
    )

    favorite_data = await FavoriteServices(session).get_favorite(
        product_id=product_id, user_id=payload_validate.userId
    )

    return {"status": "success", "favorite_data": favorite_data}


@router.delete("/{product_id}")
async def delete_favorite(
    product_id: Annotated[int, Path(gt=0)],
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="favorites:delete"
    )

    deleted_favorite = await FavoriteRepository(session).delete(
        product_id=product_id, user_id=payload_validate.userId
    )

    if not deleted_favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Don't found product_id",
        )

    return {"status": "success", "deleted_favorite": deleted_favorite}
