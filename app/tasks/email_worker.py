import json

from aio_pika.abc import AbstractIncomingMessage

from app.tasks.email import send_welcome_email_task

async def handle(message: AbstractIncomingMessage) -> None:
    async with message.process():
        event = json.loads(message.body)
        print(f'event received: {event}')
        send_welcome_email_task.delay(event['email'], event['username'])