import csv
import time
from pathlib import Path
from sqlalchemy import select, func

from app.core.config import BASE_DIR
from app.db.database import async_session_maker
from app.db.models import Post, User
from app.tasks.celery_app import celery_app
from app.tasks.utils import run_async


REPORTS_DIR = BASE_DIR / 'reports'


async def load_users_with_posts() -> list[tuple]:
    async with async_session_maker() as session:
        stmt = (
            select(User.id, User.username, User.email, func.count(Post.id))
            .outerjoin(Post, Post.author_id == User.id)
            .group_by(User.id)
            .order_by(User.id)
        )
        return (await session.execute(stmt)).all()


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=2, #(2, 4, 8, 16..)
    max_retries=5,
)
def generate_users_report(self) -> dict:
    rows = run_async(load_users_with_posts())
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f'users_{self.request.id}.csv'

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'username', 'email', 'post_count'])
        for row in rows:
            writer.writerow(row)
            time.sleep(0.1)
    return {'file': path.name, 'rows': len(rows)}

