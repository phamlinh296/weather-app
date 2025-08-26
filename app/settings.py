from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openweather_api_key: str = Field(alias="OPENWEATHER_API_KEY")
    default_lang: str = Field("vi", alias="DEFAULT_LANG")
    default_units: str = Field("metric", alias="DEFAULT_UNITS")
    cache_ttl_seconds: int = Field(600, alias="CACHE_TTL_SECONDS")
    use_redis: bool = Field(False, alias="USE_REDIS")
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
