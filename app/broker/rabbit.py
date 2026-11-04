import json
from datetime import datetime, timezone

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractRobustConnection
from fastapi import Request

from app.core.config import settings

EXCHANGE_NAME = 'auth.events'


async def connect_rabbit(name: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        settings.rabbit_url,
        client_properties={'connection_name': name}
    )


async def declare_events_exchange(channel: AbstractChannel) -> AbstractExchange:
    return await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )


class EventPublisher():
    def __init__(self, exchange: AbstractExchange) -> None:
        self.exchange = exchange

    async  def publish(self, routing_key: str, payload: dict) -> None:
        event = {
            'event': routing_key,
            'occured_at': datetime.now(timezone.utc).isoformat(),
            **payload
        }
        message = aio_pika.Message(
            body=json.dumps(event, ensure_ascii=False).encode('utf-8'),
            content_type='application/json',
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self.exchange.publish(message, routing_key)


def get_publisher(request: Request) -> EventPublisher:
    return request.app.state.publisher