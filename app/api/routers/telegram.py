import logging
import secrets
from typing import Annotated
from aiogram.types import Update
from fastapi import APIRouter, HTTPException, Header, Request, status

from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/telegram', tags=['Telegram'])

@router.post('/webhook',include_in_schema=False)
async def telegram_webhook(
        request: Request,
        x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None
):
    bot = getattr(request.app.state, 'bot', None)
    dp = getattr(request.app.state, 'dp', None)
    if bot is None or dp is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Telegram bot is not available')

    expected = settings.telegram_webhook_secret
    if expected is None or not secrets.compare_digest(
        x_telegram_bot_api_secret_token or '', expected.get_secret_value()
    ):
        logger.warning('Вебхук без правильного секрета')
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    update = Update.model_validate(await request.json(), context={'bot': bot})
    await dp.feed_update(bot, update)
    return {'ok': True}
