import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError

logger = logging.getLogger(__name__)

def problem(request: Request, status: int, detail: str,
            code: str, headers: dict | None = None, **extra) -> JSONResponse:
    request_id = getattr(request.state, 'request_id', None)
    body = {
        'type': 'about:link',
        'title': HTTPStatus(status).phrase,
        'status': status,
        'detail': detail,
        'instance': request.url.path,
        'code': code,
        'request_id': request_id,
        **extra
    }
    headers = {**(headers or {}), **({'X-Request-ID': request_id} if request_id else {})}
    return JSONResponse(status_code=status, content=body, headers=headers, media_type='application/json')


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error('%s: %s %s', exc.code, exc.message, exc.extra, exc_info=exc)
    return problem(request, exc.status_code, exc.message, exc.code, **exc.extra)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [
        {'field': '.'.join(str(p) for p in err['loc'][1:] or err['loc'][0]), 'message': err['msg'], 'type': err['type']}
         for err in exc.errors()
    ]
    return problem(
        request=request,
        status=422,
        detail='Проверьте поля запроса',
        code='validation_error',
        errors=errors

    )

async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception('Необработанная ошибка: %s %s request_id=%s',
                     request.method, request.url.path, getattr(request.state, 'request_id', None))
    return problem(
        request=request,
        status=500,
        detail='Внутренняя ошибка сервера. Сообщие request_id в поддержку',
        code='unhandled_exception',
    )


def install_error_handler(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

