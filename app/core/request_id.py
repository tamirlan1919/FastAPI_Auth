import re
import uuid

from fastapi import Request
from starlette.responses import Response

REQUEST_ID_HEADER = 'X-Request-ID'

# ID от клиента/прокси принимаем, только если он короткий и из безопасных символов:
# он попадает в логи и в тело ответа, мусор и простыни туда пускать нельзя
_VALID_REQUEST_ID = re.compile(r'^[A-Za-z0-9._-]{1,128}$')


async def request_id_middleware(request: Request, call_next) -> Response:
    incoming = request.headers.get(REQUEST_ID_HEADER)
    request_id = incoming if incoming and _VALID_REQUEST_ID.fullmatch(incoming) else uuid.uuid4().hex

    # request.state живёт в scope['state'] — его же увидят error_handler'ы, в том числе для 500
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers[REQUEST_ID_HEADER] = request_id
    return response
