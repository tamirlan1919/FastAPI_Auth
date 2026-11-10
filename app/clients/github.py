import asyncio
import httpx


async def get_user(username: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://api.github.com/users/{username}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as err:
            raise err


