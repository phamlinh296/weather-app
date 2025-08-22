from fastapi import FastAPI
from app.routers import weather_router

app = FastAPI(title="Weather API MVP")

# Đăng ký router
app.include_router(weather_router.router)
