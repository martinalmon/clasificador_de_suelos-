"""Creación de la cuenta del usuario autenticado."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import firestore
from pydantic import BaseModel, Field

from app.api.autenticacion import obtener_usuario_actual
from app.base_datos import obtener_base_datos


router = APIRouter(prefix="/account", tags=["Cuenta"])
CREDITOS_BIENVENIDA = 10


class RespuestaCuenta(BaseModel):
    uid: str
    creditos: int = Field(strict=True, ge=0)


@firestore.transactional
def crear_cuenta_si_falta(transaction, referencia):
    documento = referencia.get(transaction=transaction)

    if documento.exists:
        return documento.to_dict()

    datos = {
        "creditos": CREDITOS_BIENVENIDA,
        "bienvenida_otorgada": True,
        "creado_en": firestore.SERVER_TIMESTAMP,
    }

    transaction.create(referencia, datos)
    return datos


@router.post("/initialize", response_model=RespuestaCuenta)
def inicializar_cuenta(
        usuario: Annotated[dict, Depends(obtener_usuario_actual)],
        base_datos: Annotated[firestore.Client, Depends(obtener_base_datos)],
) -> RespuestaCuenta:
    uid = usuario["uid"]
    referencia = base_datos.collection("usuarios").document(uid)

    try:
        datos = crear_cuenta_si_falta(
            base_datos.transaction(max_attempts=5),
            referencia,
        )
    except (GoogleAPICallError, RetryError):
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la cuenta. Intenta nuevamente.",
        ) from None

    creditos = datos.get("creditos")
    if type(creditos) is not int or creditos < 0:
        raise HTTPException(
            status_code=500,
            detail="La cuenta tiene un saldo inconsistente.",
        )

    return RespuestaCuenta(uid=uid, creditos=creditos)