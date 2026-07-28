from .celery_app import celery_instance
from .tasks import update_delivery_status_task

__all__ = ["celery_instance", "update_delivery_status_task"]
