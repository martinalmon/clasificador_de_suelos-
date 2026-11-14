from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from app.api.autenticacion import obtener_usuario_actual

from app.domain.clasificador_unificado import (
    ResultadoClasificacion,
    clasificar_sucs,
)
from app.domain.muestra_suelo import MuestraSuelo


router = APIRouter(tags=["Clasificación"])


class SolicitudClasificacion(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        allow_inf_nan=False,
    )

    identificador: str
    pasa_malla_200: float
    pasa_malla_4: float | None = None
    pasa_malla_40: float | None = None
    limite_liquido: float | None = None
    limite_plastico: float | None = None
    d10: float | None = None
    d30: float | None = None
    d60: float | None = None
    inorganico_confirmado: bool = False


@router.post(
    "/classify",
    dependencies=[Depends(obtener_usuario_actual)],
)
async def clasificar(solicitud: SolicitudClasificacion) -> ResultadoClasificacion:
    """Clasifica una muestra de laboratorio mediante el motor SUCS."""
    datos_muestra = solicitud.model_dump(exclude={"inorganico_confirmado"})

    try:
        muestra = MuestraSuelo(**datos_muestra)
        return clasificar_sucs(
            muestra,
            inorganico_confirmado=solicitud.inorganico_confirmado,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error