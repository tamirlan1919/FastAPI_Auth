import asyncio
import time

import httpx
from cryptography.hazmat.primitives.ciphers import aead

LOGINS = ['tamirlan1919', 'octobat', 'gvanrossum', 'torvalds', 'samaltman']

def sync_demo():
    response = httpx.get('https://api.github.com/users/tiangolo')
    print(f'Статус {response.status_code}, {response.headers["content-type"]}')
    print(f'Лимит {response.headers["x-ratelimit-limit"]}')
    data = response.json()
    print(f'{data["name"]} | репозиториев {data["public_repos"]} | подписчиков {data["followers"]}')



async def fetch_login(login: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.github.com/users/{login}')
        return response.json()['login']


async def async_demo():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        for login in LOGINS:
            await fetch_login(login)
        print('По очереди', time.perf_counter() - start)
        start = time.perf_counter()
        result = await asyncio.gather(*(fetch_login(login) for login in LOGINS))
        print(f'Параллельно', time.perf_counter() - start, result)


async def fetch_posts():
    # Используем 'async with' для управления жизненным циклом клиента
    async with httpx.AsyncClient() as client:
        # 'await' приостанавливает выполнение, пока мы ждем ответа от сети
        response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
        # Проверить, был ли запрос успешным (статус 2xx)
        response.raise_for_status()
        print(response.json())
        return response.json()


async def main():
    await async_demo()
    await fetch_posts()

if __name__ == '__main__':
    sync_demo()
    asyncio.run(main())