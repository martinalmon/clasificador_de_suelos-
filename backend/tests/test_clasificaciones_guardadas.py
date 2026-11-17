
"""Pruebas del guardado de clasificaciones y consumo de créditos."""

import os
from uuid import uuid4

import pytest
from fastapi import HTTPException
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore

from app.clasificaciones_guardadas import guardar_clasificacion


@pytest.fixture
def entorno():
    assert os.environ.get("FIRESTORE_EMULATOR_HOST") == "127.0.0.1:8080", (
        "Estas pruebas requieren el emulador local de Firestore."
    )

    db = firestore.Client(
        project="demo-sucs-local",
        credentials=AnonymousCredentials(),
    )

    uid = f"test-clasificacion-{uuid4().hex}"
    cuenta = db.collection("usuarios").document(uid)
    cuenta.set({
        "creditos": 10,
        "bienvenida_otorgada": True,
    })

    try:
        yield db, uid, cuenta
    finally:
        for documento in cuenta.collection("clasificaciones").stream():
            documento.reference.delete()
        cuenta.delete()
        db.close()


def datos_ejemplo():
    return {
        "identificador": "MUESTRA-001",
        "pasa_malla_200": 80.0,
        "limite_liquido": 45.0,
        "limite_plastico": 22.0,
    }


def resultado_ejemplo():
    return {
        "simbolo": "CL",
        "descripcion": "Arcilla de baja plasticidad",
    }


def test_clasificacion_descuenta_un_credito(entorno):
    db, uid, cuenta = entorno

    resultado = guardar_clasificacion(
        db, uid, "operacion-001",
        datos_ejemplo(), resultado_ejemplo(),
    )

    assert resultado["simbolo"] == "CL"
    assert cuenta.get().to_dict()["creditos"] == 9
    assert len(list(cuenta.collection("clasificaciones").stream())) == 1


def test_repetir_operacion_no_descuenta_dos_veces(entorno):
    db, uid, cuenta = entorno

    for _ in range(2):
        guardar_clasificacion(
            db, uid, "misma-operacion",
            datos_ejemplo(), resultado_ejemplo(),
        )

    assert cuenta.get().to_dict()["creditos"] == 9
    assert len(list(cuenta.collection("clasificaciones").stream())) == 1


def test_operacion_reutilizada_con_otros_datos(entorno):
    db, uid, cuenta = entorno

    guardar_clasificacion(
        db, uid, "operacion-duplicada",
        datos_ejemplo(), resultado_ejemplo(),
    )

    otros_datos = datos_ejemplo()
    otros_datos["limite_liquido"] = 60.0

    with pytest.raises(HTTPException) as error:
        guardar_clasificacion(
            db, uid, "operacion-duplicada",
            otros_datos, resultado_ejemplo(),
        )

    assert error.value.status_code == 409
    assert cuenta.get().to_dict()["creditos"] == 9


def test_saldo_cero_impide_clasificar(entorno):
    db, uid, cuenta = entorno
    cuenta.update({"creditos": 0})

    with pytest.raises(HTTPException) as error:
        guardar_clasificacion(
            db, uid, "sin-creditos",
            datos_ejemplo(), resultado_ejemplo(),
        )

    assert error.value.status_code == 403
    assert cuenta.get().to_dict()["creditos"] == 0
    assert len(list(cuenta.collection("clasificaciones").stream())) == 0


def test_cuenta_inexistente(entorno):
    db, uid, cuenta = entorno
    cuenta.delete()

    with pytest.raises(HTTPException) as error:
        guardar_clasificacion(
            db, uid, "sin-cuenta",
            datos_ejemplo(), resultado_ejemplo(),
        )

    assert error.value.status_code == 409


def test_clave_operacion_vacia(entorno):
    db, uid, cuenta = entorno

    with pytest.raises(HTTPException) as error:
        guardar_clasificacion(
            db, uid, "",
            datos_ejemplo(), resultado_ejemplo(),
        )

    assert error.value.status_code == 422
    assert cuenta.get().to_dict()["creditos"] == 10


def test_saldo_inconsistente(entorno):
    db, uid, cuenta = entorno
    cuenta.update({"creditos": -1})

    with pytest.raises(HTTPException) as error:
        guardar_clasificacion(
            db, uid, "saldo-invalido",
            datos_ejemplo(), resultado_ejemplo(),
        )

    assert error.value.status_code == 500
