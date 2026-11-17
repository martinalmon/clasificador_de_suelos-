"""Consulta privada y gratuita de clasificaciones."""

import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import firestore

from app.api.autenticacion import obtener_usuario_actual
from app.base_datos import obtener_base_datos


router = APIRouter(
    prefix="/classifications",
    tags=["Historial de clasificaciones"],
)

PATRON_ID = re.compile(r"^[a-f0-9]{64}$")


def validar_id(identificador: str) -> str:
    """Valida el identificador SHA-256 de la operacion."""
    if not PATRON_ID.fullmatch(identificador):
        raise HTTPException(
            status_code=422,
            detail="Identificador de clasificacion invalido.",
        )
    return identificador


def referencia_historial(db, uid: str):
    return (
        db.collection("usuarios")
        .document(uid)
        .collection("clasificaciones")
    )


def serializar(documento):
    datos = documento.to_dict()

    fecha = datos.get("creado_en")

    if fecha is not None:
        fecha = fecha.isoformat()

    return {
        "id": documento.id,
        "entrada": datos.get("entrada"),
        "resultado": datos.get("resultado"),
        "creditos_consumidos": datos.get(
            "creditos_consumidos", 1
        ),
        "creado_en": fecha,
    }


@router.get("")
def listar_clasificaciones(
    usuario: Annotated[
        dict, Depends(obtener_usuario_actual)
    ],
    db: Annotated[
        firestore.Client, Depends(obtener_base_datos)
    ],
    limite: Annotated[
        int, Query(ge=1, le=50)
    ] = 20,
    cursor: str | None = None,
):
    """Lista resultados propios sin consumir creditos."""

    coleccion = referencia_historial(
        db, usuario["uid"]
    )

    try:
        consulta = coleccion.order_by(
            "creado_en",
            direction=firestore.Query.DESCENDING,
        )

        if cursor is not None:
            validar_id(cursor)

            anterior = coleccion.document(cursor).get()

            if not anterior.exists:
                raise HTTPException(
                    status_code=400,
                    detail="Cursor no valido para este usuario.",
                )

            consulta = consulta.start_after(anterior)

        documentos = list(
            consulta.limit(limite + 1).stream()
        )

        hay_mas = len(documentos) > limite
        pagina = documentos[:limite]

        siguiente_cursor = None

        if hay_mas and pagina:
            siguiente_cursor = pagina[-1].id

        return {
            "elementos": [
                serializar(doc) for doc in pagina
            ],
            "siguiente_cursor": siguiente_cursor,
            "hay_mas": hay_mas,
        }

    except GoogleAPICallError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar el historial.",
        ) from None


@router.get("/{clasificacion_id}")
def obtener_clasificacion(
    clasificacion_id: str,
    usuario: Annotated[
        dict, Depends(obtener_usuario_actual)
    ],
    db: Annotated[
        firestore.Client, Depends(obtener_base_datos)
    ],
):
    """Obtiene una clasificacion propia sin cobrar creditos."""

    validar_id(clasificacion_id)

    referencia = referencia_historial(
        db, usuario["uid"]
    ).document(clasificacion_id)

    try:
        documento = referencia.get()
    except GoogleAPICallError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la clasificacion.",
        ) from None

    if not documento.exists:
        raise HTTPException(
            status_code=404,
            detail="Clasificacion no encontrada.",
        )

    return serializar(documento)