import asyncio


class EmailSendError(Exception):
    pass


async def send_welcome_email(email: str, username: str) -> None:
    await asyncio.sleep(3)
    if email.startswith('fail'):
        raise EmailSendError(f'SMTP недступен, письмо для {username} не ушло')
    print(f'Письмо "Добро пожаловать {username}!" Отправлено на {email}')