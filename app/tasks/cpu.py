from app.core.security import hash_password
from app.tasks.celery_app import celery_app

@celery_app.task
def hash_passwords(count: int) -> int:
    for _ in range(count):
        hash_password('Super-secret123')
    return count

