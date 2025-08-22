 # Controller (FastAPI routers)
from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.weather_models import WeatherResponse, DailyForecastResponse, HourlyForecastResponse
from app.client.openweather_client import OpenWeatherClient
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

client = OpenWeatherClient()
service = WeatherService(client)

@router.get("/current", response_model=WeatherResponse)
def current_weather(city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None):
    return service.get_current_weather(city, lat, lon)

@router.get("/forecast/daily", response_model=List[DailyForecastResponse])
def daily_forecast(city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None, days: int = Query(3, ge=1, le=7)):
    return service.get_daily_forecast(city, lat, lon, days)

@router.get("/forecast/hourly", response_model=List[HourlyForecastResponse])
def hourly_forecast(city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None, hours: int = Query(24, ge=1, le=48)):
    return service.get_hourly_forecast(city, lat, lon, hours)
