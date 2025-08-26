from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware


from app.settings import settings
from app.cache import InMemoryCache
from app.services.weather_client import WeatherClient
from app.schemas import ForecastResponse, ErrorResponse, HourlySlice, TomorrowSummary
from app.utils import to_local_date, mode_text


from datetime import datetime, timedelta
from typing import List


app = FastAPI(title="Weather App", version="1.0.0")


# CORS if you want to call API from another frontend
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


cache = InMemoryCache()
client = WeatherClient()


@app.on_event("shutdown")
async def shutdown_event():
	await client.aclose()




@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request, "result": None, "error": None})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, city: str = Query(..., min_length=2)):
    key = f"forecast:{city.lower()}"
    cached = cache.get(key)
    if cached:
        result = cached
    else:
        try:
            data = await client.get_forecast(city)
        except ValueError:
            # Nếu city không hợp lệ
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "result": None, "error": "City không hợp lệ"}
            )
        except RuntimeError:
            # Nếu API key sai
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "result": None, "error": "API key không hợp lệ"}
            )

        # Map data raw từ OpenWeather sang format template bạn muốn
        result = {
            "city": data["city"]["name"],
            "country": data["city"].get("country", ""),
            "summary": {
                "date": data["list"][0]["dt_txt"].split(" ")[0],
                "temp_min": min([x["main"]["temp_min"] for x in data["list"]]),
                "temp_max": max([x["main"]["temp_max"] for x in data["list"]]),
                "description": data["list"][0]["weather"][0]["description"],
                "pop_max": max([x.get("pop", 0) for x in data["list"]])
            },
            "hourly": [
                {
                    "time": x["dt_txt"],
                    "temp": x["main"]["temp"],
                    "description": x["weather"][0]["description"],
                    "pop": x.get("pop", 0)
                } for x in data["list"]
            ]
        }

        cache.set(key, result)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result, "error": None}
    )

@app.get("/api/forecast", response_model=ForecastResponse, responses={400: {"model": ErrorResponse}})
async def api_forecast(city: str = Query(..., min_length=2)):
	key = f"forecast:{city.lower()}"
	cached = cache.get(key)
	if cached:
		return cached

	data = await client.get_forecast(city)

	city_name = data["city"]["name"]
	country = data["city"].get("country", "")
	tz_offset = data["city"].get("timezone", 0)

	# Group entries by local date
	by_date: dict[str, list[dict]] = {}
	for entry in data["list"]:
		d = to_local_date(entry["dt_txt"], tz_offset)
		by_date.setdefault(d, []).append(entry)

	# Pick tomorrow
	today = (datetime.utcnow() + timedelta(seconds=tz_offset)).date()
	tomorrow_str = (today + timedelta(days=1)).isoformat()
	return templates.TemplateResponse("index.html", {"request": request, "result": None, "error": "City không hợp lệ"})