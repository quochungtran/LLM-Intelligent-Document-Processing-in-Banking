import os

from celery import Celery
from config import Config
from celery import shared_task

def get_celery_app(name):
    # Create a Celery app instance
    app = Celery(
        name,
        broker=Config.CELERY_BROKER_URL,  # Redis as the message broker
        backend=Config.CELERY_RESULT_BACKEND  # Redis as the result backend
    )

    # Optionally, you can configure additional settings here
    app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='Asia/Ho_Chi_Minh',  # Set to a city in UTC+7
        enable_utc=True
    )

    # Configure Celery logging
    app.conf.update(
        worker_hijack_root_logger=False,
        worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
        worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    )

    return app


# Discover tasks from submodules
celery_app = get_celery_app(__name__)
celery_app.autodiscover_tasks(['src.task.calculation_task', 'src.task.routing_task', 'src.task.rag_task', 'src.task.agent_task'])