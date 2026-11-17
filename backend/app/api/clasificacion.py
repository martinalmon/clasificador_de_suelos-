"""API de clasificacion SUCS con consumo de creditos."""

from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import firestore
from pydantic import BaseModel, ConfigDict

from app.api.autenticacion import obtener_usuario_actual
from app.base_datos import obtener_base_datos
from app.clasificaciones_guardadas import guardar_clasificacion
from app.domain.clasificador_unificado import (
    ResultadoClasificacion,
    clasificar_sucs,
)
from app.domain.muestra_suelo import MuestraSuelo


router = APIRouter(tags=["Clasificacion"])


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
    response_model=ResultadoClasificacion,
)
def clasificar(
    solicitud: SolicitudClasificacion,
    usuario: Annotated[
        dict,
        Depends(obtener_usuario_actual),
    ],
    base_datos: Annotated[
        firestore.Client,
        Depends(obtener_base_datos),
    ],
    clave_operacion: Annotated[
        str,
        Header(
            alias="Idempotency-Key",
            min_length=1,
            max_length=128,
        ),
    ],
) -> dict:
    """Clasifica, guarda y cobra un credito por operacion nueva."""

    datos_entrada = solicitud.model_dump()

    datos_muestra = solicitud.model_dump(
        exclude={"inorganico_confirmado"}
    )

    try:
        muestra = MuestraSuelo(**datos_muestra)

        resultado = clasificar_sucs(
            muestra,
            inorganico_confirmado=(
                solicitud.inorganico_confirmado
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    resultado_dict = asdict(resultado)

    try:
        return guardar_clasificacion(
            base_datos=base_datos,
            uid=usuario["uid"],
            clave_operacion=clave_operacion,
            datos_entrada=datos_entrada,
            resultado=resultado_dict,
        )

    except (GoogleAPICallError, RetryError):
        raise HTTPException(
            status_code=503,
            detail=(
                "No se pudo guardar la clasificacion. "
                "Reintenta con la misma clave de operacion."
            ),
        ) from None