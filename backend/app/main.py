"""Punto de entrada HTTP de GeoStratix."""

from fastapi import FastAPI
from app.api.cuenta import router as cuenta_router


from app.api.clasificacion import router as clasificacion_router
from app.api.health import router as health_router

from app.api.autenticacion import router as autenticacion_router



app = FastAPI(title="GeoStratix API", version="0.1.0")

app.include_router(health_router)
app.include_router(clasificacion_router)
app.include_router(autenticacion_router)
app.include_router(cuenta_router)

from app.api.historial import router as historial_router
app.include_router(historial_router)
