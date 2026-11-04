import asyncio
import json

from aio_pika.abc import AbstractIncomingMessage

from app.broker.rabbit import connect_rabbit, declare_events_exchange
from app.services.email_service import send_welcome_email


QUEUE_NAME = 'email.welcome'


async def handle(message: AbstractIncomingMessage) -> None:
    async with message.process():
        event = json.loads(message.body)
        print(f'Получено событие {event["event"]} для {event["email"]}')
        await send_welcome_email(event["email"], event["username"])


async def main():
    connection = await connect_rabbit('email-worker')
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        exchange = await declare_events_exchange(channel)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.bind(exchange, routing_key='user.registered')

        print(f'email-worker слушает очередь {QUEUE_NAME}. Остановить CTRL+C')
        async with queue.iterator() as messages:
            async for message in messages:
                await handle(message)


if __name__ == '__main__':
    asyncio.run(main())