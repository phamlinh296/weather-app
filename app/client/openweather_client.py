# Tích hợp external API (OpenWeatherMap, AccuWeather...)
import requests
from datetime import datetime, date
from typing import List
from app.models.weather_models import WeatherResponse, DailyForecastResponse, HourlyForecastResponse
from app.config.settings import settings

class OpenWeatherClient:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.BASE_URL

    def _build_params(self, city=None, lat=None, lon=None):
        params = {"appid": self.api_key, "units": "metric", "lang": "vi"}
        if city:
            params["q"] = city
        elif lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        return params

    def fetch_current_weather(self, city=None, lat=None, lon=None) -> WeatherResponse:
        url = f"{self.base_url}/weather"
        res = requests.get(url, params=self._build_params(city, lat, lon))
        data = res.json()

        return WeatherResponse(
            city=data["name"],
            temperature=data["main"]["temp"],
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            timestamp=datetime.fromtimestamp(data["dt"])
        )

    def fetch_daily_forecast(self, city=None, lat=None, lon=None, days=3) -> List[DailyForecastResponse]:
        url = f"{self.base_url}/forecast/daily"
        res = requests.get(url, params={**self._build_params(city, lat, lon), "cnt": days})
        data = res.json()

        return [
            DailyForecastResponse(
                date=date.fromtimestamp(d["dt"]),
                min_temp=d["temp"]["min"],
                max_temp=d["temp"]["max"],
                description=d["weather"][0]["description"]
            )
            for d in data["list"]
        ]

    def fetch_hourly_forecast(self, city=None, lat=None, lon=None, hours=24) -> List[HourlyForecastResponse]:
        url = f"{self.base_url}/forecast"
        res = requests.get(url, params=self._build_params(city, lat, lon))
        data = res.json()

        return [
            HourlyForecastResponse(
                datetime=datetime.fromtimestamp(d["dt"]),
                temperature=d["main"]["temp"],
                description=d["weather"][0]["description"]
            )
            for d in data["list"][:hours]
        ]
