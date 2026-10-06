from unittest.mock import AsyncMock, patch

import pytest
import httpx

from app.clients.weather import get_weather_data

@pytest.mark.asyncio
@patch("app.clients.weather.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_weather_data(mock_get):
    mock_get.return_value = httpx.Response(
        200,
        json={'city': 'Paris', 'temp': 20},
        request=httpx.Request("GET", "https://api.weather.com/forecast/Paris"),
    )
    data = await get_weather_data("Paris")
    assert data['temp'] == 20

    mock_get.assert_called_once_with('https://api.weather.com/forecast/Paris')


