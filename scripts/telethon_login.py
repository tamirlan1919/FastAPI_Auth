from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from app.core.config import settings

def main() -> None:
    if not settings.telegram_api_id or not settings.telegram_api_hash:
        raise SystemExit('Сначала telegram_id and Telegram_Hash положи в .env')

    with TelegramClient(StringSession(), settings.telegram_api_id,
                        settings.telegram_api_hash.get_secret_value()) as client:
        me = client.get_me()
        print(f'Вошли как {me.first_name}')


if __name__ == '__main__':
    main()