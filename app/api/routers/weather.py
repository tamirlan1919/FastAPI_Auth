import httpx
from fastapi import APIRouter, HTTPException
from app.clients.weather import get_weather_data
from app.schemas.weather import WeatherApiResponse

router = APIRouter(prefix='/weather', tags=['weather'])

@router.get('/{city}', response_model=WeatherApiResponse)
async def get_weather(city: str):
    try:
        data = await get_weather_data(city)
        return data
    except httpx.TimeoutException:
        # Ошибка таймаута
        raise HTTPException(status_code=504, detail="Внешний сервис не ответил вовремя.")
    except httpx.ConnectError:
        # Ошибка соединения
        raise HTTPException(status_code=503, detail="Не удалось подключиться к внешнему сервису.")
    except httpx.HTTPStatusError as e:
        # Ошибка со статусом 4xx или 5xx
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Внешний сервис вернул ошибку: {e.response.text}"
        )
