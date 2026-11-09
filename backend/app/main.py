"""Punto de entrada HTTP; no incluye reglas de clasificación."""

from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(title="GeoStratix API", version="0.1.0")
app.include_router(health_router)
