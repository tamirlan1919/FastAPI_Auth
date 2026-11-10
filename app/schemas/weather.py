from pydantic import BaseModel, Field


# 1. Создаем Pydantic-модели на основе документации API
class WeatherDescription(BaseModel):
    main: str
    description: str


class MainWeatherData(BaseModel):
    temp: float
    # validation_alias — как поле называется во ВХОДНЫХ данных (ответ OpenWeather),
    # serialization_alias — как оно будет называться в НАШЕМ ответе клиенту.
    feels_like: float = Field(validation_alias="feels_like", serialization_alias="feelsLike")
    temp_min: float = Field(validation_alias="temp_min", serialization_alias="tempMin")
    humidity: int


class WeatherApiResponse(BaseModel):
    weather: list[WeatherDescription]  # OpenWeather отдаёт массив условий
    main: MainWeatherData
    name: str
