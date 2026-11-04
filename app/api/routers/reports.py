from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.tasks.celery_app import celery_app
from app.tasks.reports import REPORTS_DIR, generate_users_report

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post('/users', status_code=status.HTTP_202_ACCEPTED)
def create_users_report():
    task = generate_users_report.delay()
    return {'task_id': task.id, 'status_url': f'/reports/tasks/{task.id}'}


@router.get('/tasks/{task_id}', status_code=status.HTTP_200_OK)
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    response = {'task_id': result.task_id, 'status': result.status}
    if result.status == 'PROGRESS':
        response['progress'] = result.info
    elif result.successful():
        response['result'] = result.result
    elif result.failed():
        response['error'] = str(result.result)

    return response