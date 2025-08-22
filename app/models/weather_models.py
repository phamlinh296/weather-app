 # DTO / Schema (Pydantic)
from pydantic import BaseModel
from datetime import datetime, date

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: float
    wind_speed: float
    timestamp: datetime

class DailyForecastResponse(BaseModel):
    date: date
    min_temp: float
    max_temp: float
    description: str

class HourlyForecastResponse(BaseModel):
    datetime: datetime
    temperature: float
    description: str
