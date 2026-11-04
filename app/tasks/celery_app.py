import os


from kombu import Exchange, Queue
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_init

from app.core.config import settings

# On macOS billiard starts prefork children via spawn instead of fork. Without this
# flag Celery skips initializing them and every task fails with
# "ValueError: not enough values to unpack (expected 3, got 0)".
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

celery_app = Celery(
    'auth-api',
    broker=settings.rabbit_url,
    backend=settings.celery_result_backend,
    include=['app.tasks.demo', 'app.tasks.reports', 'app.tasks.cpu', 'app.tasks.email']
)

DLX = Exchange('celery.dlx', type='fanout')
DLQ = Queue('celery.dlq', DLX, durable=True)


celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
    timezone ='UTC',
    # RabbitMQ 4.x denies transient non-exclusive queues (transient_nonexcl_queues),
    # so Celery's pidbox (mingle/inspect) and gossip queues must be exclusive.
    control_queue_exclusive=True,
    event_queue_exclusive=True,

    task_queues=[
        # Without routing_key Celery binds every queue with the same key ('default'),
        # so one message would be copied into all queues.
        Queue('default', routing_key='default'),
        Queue('reports', routing_key='reports'),
        Queue('emails', routing_key='emails', queue_arguments = {
            'x-dead-letter-exchange': 'celery.dlx',
            'x-max-priority': 10
        }),

    ],
    task_default_queue='default',
    task_routes={
        'app.tasks.reports.*': {'queue': 'reports'},
        'app.tasks.email.*': {'queue': 'emails'},
    },
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_acks_on_failure_or_timeout=True,

)

@worker_init.connect
def declare_dlq(**kwargs):
    with celery_app.connection() as conn:
        DLQ.bind(conn.default_channel).declare()




celery_app.conf.beat_schedule = {
    'send-report-every-morning': {
        'task': 'app.tasks.reports.generate_users_report',
        'schedule': crontab(hour=21, minute=38), # Каждый день в 21:38
    },
}