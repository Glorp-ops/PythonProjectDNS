from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..celery_tasks import update_delivery_status_task
from ..database.sqlalchemy_connect import get_session
from ..schemes import OrdersScheme, pagination
from ..services import check_users_sessions
from ..services.services_layer import SystemOrderService

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("", status_code=201)
async def create_order(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    order: OrdersScheme,
):
    payload_validate, _ = await check_users_sessions(
        session=session, request=request, permission="orders:create_own"
    )

    order_data = await SystemOrderService(session).create_order(
        order.delivery_address,
        order.delivery_method,
        user_id=payload_validate.userId,
        products_id=order.products_id,
    )

    update_delivery_status_task.delay(
        order_id=order_data[0].order_id, user_id=payload_validate.userId
    )

    return order_data


@router.get("")
async def get_orders(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    pagination: pagination,
):
    payload_validate, _ = await check_users_sessions(
        session=session, request=request, permission="orders:view_own"
    )

    orders_data, pagination_settings = await SystemOrderService(session).get_orders(
        user_id=payload_validate.userId, page=pagination.page, size=pagination.size
    )

    return {"data": orders_data, "pagination": pagination_settings}


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session=session, request=request, permission="orders:view_own"
    )

    return await SystemOrderService(session).get_order(
        order_id=order_id, user_id=payload_validate.userId
    )


@router.patch("/cancellation/{order_id}")
async def delete_order(
    order_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session=session, request=request, permission="orders:cancel_own"
    )

    await SystemOrderService(session).update_check_delivery_status(
        order_id, status="отменен", user_id=payload_validate.userId
    )

    return {
        "result": "true",
        "order_data": {"order_id": order_id, "order_status": "отменен"},
    }
