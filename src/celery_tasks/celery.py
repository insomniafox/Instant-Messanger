from celery import Celery

from src.core.config import settings


celery_app = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}',
    include=['src.celery_tasks.tasks']
)
