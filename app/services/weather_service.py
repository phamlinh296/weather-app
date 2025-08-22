from typing import List
from app.models.weather_models import WeatherResponse, DailyForecastResponse, HourlyForecastResponse
from app.client.openweather_client import OpenWeatherClient

class WeatherService:
    def __init__(self, client: OpenWeatherClient):
        self.client = client

    def get_current_weather(self, city=None, lat=None, lon=None) -> WeatherResponse:
        return self.client.fetch_current_weather(city, lat, lon)

    def get_daily_forecast(self, city=None, lat=None, lon=None, days=3) -> List[DailyForecastResponse]:
        return self.client.fetch_daily_forecast(city, lat, lon, days)

    def get_hourly_forecast(self, city=None, lat=None, lon=None, hours=24) -> List[HourlyForecastResponse]:
        return self.client.fetch_hourly_forecast(city, lat, lon, hours)
