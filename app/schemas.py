from pydantic import BaseModel
from typing import List, Optional


class HourlySlice(BaseModel):
	time: str
	temp: float
	description: str
	pop: float # probability of precipitation (0..1)


class TomorrowSummary(BaseModel):
	date: str
	temp_min: float
	temp_max: float
	description: str
	pop_max: float


class ForecastResponse(BaseModel):
	city: str
	country: str
	timezone: int
	summary: TomorrowSummary
	hourly: List[HourlySlice]


class ErrorResponse(BaseModel):
	detail: str