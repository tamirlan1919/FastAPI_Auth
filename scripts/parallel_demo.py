import asyncio
import time

from app.core.security import hash_password
from app.tasks.cpu import hash_passwords


async def io_job():
    await asyncio.sleep(0.3)


async def cpu_job():
    hash_password('Super-secret123')


async def main():
    t = time.perf_counter()
    await asyncio.gather(*[io_job() for _ in range(8)])
    print(f'8 I/O задач через asyncio: {time.perf_counter() - t:.2f} с')

    t = time.perf_counter()
    await asyncio.gather(*[cpu_job() for _ in range(8)])

    print(f'8 CPU задач через asyncio: {time.perf_counter() - t:.2f} с')


asyncio.run(main())


t = time.perf_counter()
results = [hash_passwords.delay(2) for _ in range(8)]

for r in results:
    r.get(timeout=60)

print(f'8 CPU задача через Celery: {time.perf_counter() - t:.2f} с')