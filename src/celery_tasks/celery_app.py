from celery import Celery
from celery.schedules import crontab

from ..core import settings

celery_instance = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["src.celery_tasks.tasks"],
)
celery_instance.conf.beat_schedule = {
    "beat_mod": {
        "task": "src.celery_tasks.tasks.cleanup_expired_bans_and_sessions_task",
        "schedule": crontab(hour=0, minute=0),
    }
}
