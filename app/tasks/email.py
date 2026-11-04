from app.services.email_service import send_welcome_email
from app.tasks.celery_app import celery_app
from app.tasks.utils import run_async

@celery_app.task(
    bind=True,
    max_retries=3,
    soft_time_limit=40,
    time_limit=60,
    autoretry_for=(Exception,),
)
def send_welcome_email_task(email: str, username: str) -> str:
    run_async(send_welcome_email(email, username))
    return f'sent email to {email}'


t.apply_async(args=(f'vip@ex.com', f'user'), priority=1)
t.apply_async(args=(f'promo@ex.com', f'user'), priority=9)