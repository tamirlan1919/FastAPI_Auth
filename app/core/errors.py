

class AppError(Exception):
    status_code: int = 500
    code: str = 'internal_error'
    message: str = 'Внутренняя ошибка сервера'


    def __init__(self, message: str | None = None, *, extra: dict = None) -> None:
        self.message = message or self.message
        self.extra = extra or {}
        super().__init__(message)



class BadRequest(AppError):
    status_code = 400
    code = 'bad_request'
    message = 'Некорректный запрос'


class NotFound(AppError):
    status_code = 404
    code = 'not_found'
    message = 'Не найдено'


class ConflictError(AppError):
    status_code = 409
    code = 'conflict'
    message = 'Конфликт с текущим состоянием данных'


class ExternalServiceError(AppError):
    status_code = 502
    code = 'external_service_error'
    message = 'Внешний сервис упал с ошибкой'

    def __init__(self, message: str | None = None, service: str | None = None, *, extra: dict = None) -> None:
        super().__init__(message, extra = {'service': service})


class ExternalServiceUnavailableError(ExternalServiceError):
    status_code = 503
    code = 'external_service_unavailable'
    message = 'Внешний сервис недоступен'


class ExternalServiceTimeoutError(ExternalServiceError):
    status_code = 504
    code = 'external_service_timeout'
    message = 'Внешний сервис не ответил вовремя'
