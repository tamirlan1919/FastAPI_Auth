import httpx
import asyncio


async def get_weather_data(city: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('https://openweathermap.org/data/2.5/weather', params={'q': city})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as err:
            raise err



