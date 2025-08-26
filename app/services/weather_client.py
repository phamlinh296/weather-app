import httpx
from typing import Any, Dict
from app.settings import settings


BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherClient:
	def __init__(self):
		self._client = httpx.AsyncClient(timeout=10)

	async def get_forecast(self, city: str, units: str | None = None, lang: str | None = None) -> Dict[str, Any]:
		params = {
			"q": city,
			"appid": settings.openweather_api_key,
			"units": units or settings.default_units,
			"lang": lang or settings.default_lang,
		}
		r = await self._client.get(BASE_URL, params=params)
		# Normalize common error shapes
		if r.status_code == 401:
			raise RuntimeError("Invalid OpenWeather API key")
		if r.status_code == 404:
			raise ValueError("City not found")
		r.raise_for_status()
		return r.json()

	async def aclose(self):
		await self._client.aclose()