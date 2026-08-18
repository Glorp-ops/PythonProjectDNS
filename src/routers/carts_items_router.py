from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from ..data_mappers.data_mappers_repository import CartsItemsMapper
from ..database.repositories_db import CartsItemsRepository
from ..database.sqlalchemy_connect import get_session
from ..schemes import CartItem, ChangeQuantity, pagination
from ..services import check_users_sessions
from ..services.services_layer import CartsItemsService

router = APIRouter(prefix="/api/v1/items", tags=["carts-items"])


@router.post(
    "",
    response_model=CartsItemsMapper,
    response_model_exclude_none=True,
    status_code=201,
)
async def add_cart(
    product: CartItem,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="cart:create"
    )

    carts_items = await CartsItemsService(session).add_cart_item(
        product_id=product.product_id,
        user_id=payload_validate.userId,
    )

    return carts_items


@router.get("")
async def get_carts(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    pagination: pagination,
):

    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="cart:view"
    )

    (
        cart_items_data,
        cart_data,
        summary,
        cart_is_active,
        pagination_settings,
    ) = await CartsItemsRepository(session).get_data_cart_and_cart_items(
        user_id=payload_validate.userId, page=pagination.page, size=pagination.size
    )

    return {
        **cart_data,
        "items": cart_items_data,
        "summary": summary,
        "is_active": cart_is_active,
        "pagination": pagination_settings,
    }


@router.delete(
    "/{item_id}",
    response_model=list[CartsItemsMapper],
    response_model_exclude_none=True,
)
async def delete_items(
    item_id: Annotated[int, Path(gt=0)],
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="cart:delete"
    )

    deleted_items = await CartsItemsService(session).delete_cart_item(
        item_id=item_id, user_id=payload_validate.userId
    )

    return deleted_items


@router.patch(
    "/quantity",
    response_model=CartsItemsMapper,
    response_model_exclude_none=True,
)
async def change_quantity(
    product_quantity: ChangeQuantity,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="cart:update"
    )

    updated_item = await CartsItemsService(session).update_quantity(
        item_id=product_quantity.item_id,
        quantity=product_quantity.quantity,
        user_id=payload_validate.userId,
    )

    return updated_item


@router.delete(
    "",
    response_model=list[CartsItemsMapper],
    response_model_exclude_none=True,
)
async def delete_all_items(
    session: Annotated[AsyncSession, Depends(get_session)], request: Request
):

    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="cart:delete"
    )

    deleted_all_items = await CartsItemsService(session).delete_all_cart_items(
        user_id=payload_validate.userId
    )

    return deleted_all_items
