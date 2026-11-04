import time

from app.tasks.celery_app import celery_app


@celery_app.task
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y