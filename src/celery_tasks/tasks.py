from asyncio import run, sleep
from datetime import datetime
from uuid import UUID

from dateutil.tz import UTC
from sqlalchemy import delete

from ..celery_tasks import celery_instance
from ..database.repositories_db import BlackListRepository, SessionRepository
from ..database.sqlalchemy_connect import async_session_null_pool
from ..services.services_layer import SystemOrderService


async def helper_update_delivery_status(order_id: int, status: str, user_id: UUID):

    async with async_session_null_pool() as session:
        await SystemOrderService(session).update_check_delivery_status(
            order_id, status, user_id
        )


async def helper_cleanup_expired_bans_and_sessions():
    async with async_session_null_pool() as session:
        await session.execute(
            delete(SessionRepository.model).where(
                SessionRepository.model.expires_at < datetime.now(UTC)
            )
        )
        await session.execute(
            delete(BlackListRepository.model).where(
                BlackListRepository.model.ban_until < datetime.now(UTC)
            )
        )


@celery_instance.task(bind=True, max_retries=3, default_retry_delay=2)
def update_delivery_status_task(self, order_id: int, user_id: UUID):
    try:
        run(sleep(20))
        run(helper_update_delivery_status(order_id, "доставляется", user_id))

        run(sleep(60))
        run(helper_update_delivery_status(order_id, "заказ доставлен", user_id))

        run(sleep(120))
        run(helper_update_delivery_status(order_id, "Заказ выдан", user_id))

    except Exception as e:
        raise self.retry(exc=e) from e


@celery_instance.task()
def cleanup_expired_bans_and_sessions_task():
    run(helper_cleanup_expired_bans_and_sessions())
