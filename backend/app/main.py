"""Punto de entrada HTTP de GeoStratix."""

from fastapi import FastAPI

from app.api.clasificacion import router as clasificacion_router
from app.api.health import router as health_router


app = FastAPI(title="GeoStratix API", version="0.1.0")

app.include_router(health_router)
app.include_router(clasificacion_router)