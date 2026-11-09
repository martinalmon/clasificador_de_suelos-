"""Verificación mínima de disponibilidad del servicio."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "geostratix-api"}
