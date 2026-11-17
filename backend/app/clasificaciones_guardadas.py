"""Guardado de clasificaciones y consumo transaccional de créditos."""

from hashlib import sha256

from fastapi import HTTPException
from google.cloud import firestore


@firestore.transactional
def guardar_en_transaccion(
    transaction,
    cuenta_ref,
    clasificacion_ref,
    datos_entrada,
    resultado,
):
    guardado = clasificacion_ref.get(transaction=transaction)

    if guardado.exists:
        datos_guardados = guardado.to_dict()

        if datos_guardados["entrada"] != datos_entrada:
            raise HTTPException(
                status_code=409,
                detail="La clave de operación ya se utilizó con otros datos.",
            )

        return datos_guardados["resultado"]

    cuenta = cuenta_ref.get(transaction=transaction)

    if not cuenta.exists:
        raise HTTPException(
            status_code=409,
            detail="Inicializa tu cuenta antes de clasificar.",
        )

    creditos = cuenta.to_dict().get("creditos")

    if type(creditos) is not int or creditos < 0:
        raise HTTPException(
            status_code=500,
            detail="La cuenta tiene un saldo inconsistente.",
        )

    if creditos == 0:
        raise HTTPException(
            status_code=403,
            detail="No tienes créditos disponibles.",
        )

    transaction.create(
        clasificacion_ref,
        {
            "entrada": datos_entrada,
            "resultado": resultado,
            "creditos_consumidos": 1,
            "creado_en": firestore.SERVER_TIMESTAMP,
        },
    )

    transaction.update(
        cuenta_ref,
        {"creditos": creditos - 1},
    )

    return resultado


def guardar_clasificacion(
    base_datos,
    uid: str,
    clave_operacion: str,
    datos_entrada: dict,
    resultado: dict,
) -> dict:
    """Guarda una operación del usuario y devuelve su resultado."""
    if (
        not isinstance(clave_operacion, str)
        or not clave_operacion.strip()
        or len(clave_operacion) > 128
    ):
        raise HTTPException(
            status_code=422,
            detail="La clave de operación debe tener entre 1 y 128 caracteres.",
        )

    identificador_operacion = sha256(
        clave_operacion.encode("utf-8")
    ).hexdigest()

    cuenta_ref = base_datos.collection("usuarios").document(uid)
    clasificacion_ref = cuenta_ref.collection("clasificaciones").document(
        identificador_operacion
    )

    return guardar_en_transaccion(
        base_datos.transaction(max_attempts=5),
        cuenta_ref,
        clasificacion_ref,
        datos_entrada,
        resultado,
    )