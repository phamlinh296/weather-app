# Cấu hình (API key, settings)
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "YOUR_OPENWEATHERMAP_KEY"
    BASE_URL: str = "https://api.openweathermap.org/data/2.5"

settings = Settings()

