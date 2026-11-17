"""Pruebas de integracion de la API con Firestore."""

import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore

from app.api.autenticacion import obtener_usuario_actual
from app.base_datos import obtener_base_datos
from app.main import app


cliente = TestClient(app)

MUESTRA_FINA = {
    "identificador": "F-001",
    "limite_liquido": 250,
    "limite_plastico": 45,
    "pasa_malla_4": 100,
    "pasa_malla_40": 80,
    "pasa_malla_200": 70,
    "inorganico_confirmado": True,
}

MUESTRA_GRAVA = {
    "identificador": "G-001",
    "pasa_malla_4": 30,
    "pasa_malla_200": 2,
    "d10": 0.1,
    "d30": 0.3,
    "d60": 0.6,
    "inorganico_confirmado": True,
}


def cabecera():
    return {"Idempotency-Key": str(uuid4())}


@pytest.fixture
def cuenta_prueba():
    assert os.environ.get(
        "FIRESTORE_EMULATOR_HOST"
    ) == "127.0.0.1:8080"

    db = firestore.Client(
        project="demo-sucs-local",
        credentials=AnonymousCredentials(),
    )

    uid = f"test-api-{uuid4().hex}"
    cuenta = db.collection("usuarios").document(uid)

    cuenta.set({
        "creditos": 10,
        "bienvenida_otorgada": True,
    })

    app.dependency_overrides[obtener_usuario_actual] = (
        lambda: {"uid": uid}
    )

    app.dependency_overrides[obtener_base_datos] = (
        lambda: db
    )

    try:
        yield db, cuenta

    finally:
        app.dependency_overrides.clear()

        for documento in cuenta.collection(
            "clasificaciones"
        ).stream():
            documento.reference.delete()

        cuenta.delete()
        db.close()


def saldo(cuenta):
    return cuenta.get().to_dict()["creditos"]


def test_clasifica_muestra_fina(cuenta_prueba):
    _, cuenta = cuenta_prueba

    respuesta = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers=cabecera(),
    )

    assert respuesta.status_code == 200, respuesta.text

    resultado = respuesta.json()

    assert resultado["identificador"] == "F-001"
    assert resultado["simbolo"] == "CH"
    assert resultado["tipo_suelo"] == "fino"
    assert resultado["porcentaje_finos"] == 70
    assert resultado["indice_plasticidad"] == 205
    assert isinstance(resultado["advertencias"], list)
    assert saldo(cuenta) == 9


def test_clasifica_grava(cuenta_prueba):
    _, cuenta = cuenta_prueba

    respuesta = cliente.post(
        "/classify",
        json=MUESTRA_GRAVA,
        headers=cabecera(),
    )

    assert respuesta.status_code == 200, respuesta.text
    assert respuesta.json()["simbolo"] == "GW"
    assert respuesta.json()["tipo_suelo"] == "grava"
    assert saldo(cuenta) == 9


def test_dos_clasificaciones_consumen_dos_creditos(
    cuenta_prueba,
):
    _, cuenta = cuenta_prueba

    for _ in range(2):
        respuesta = cliente.post(
            "/classify",
            json=MUESTRA_FINA,
            headers=cabecera(),
        )
        assert respuesta.status_code == 200, respuesta.text

    assert saldo(cuenta) == 8


def test_reintento_no_consume_credito(cuenta_prueba):
    _, cuenta = cuenta_prueba

    headers = cabecera()

    primera = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers=headers,
    )

    segunda = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers=headers,
    )

    assert primera.status_code == 200, primera.text
    assert segunda.status_code == 200, segunda.text
    assert primera.json() == segunda.json()
    assert saldo(cuenta) == 9


def test_misma_clave_distintos_datos(cuenta_prueba):
    _, cuenta = cuenta_prueba

    headers = cabecera()

    primera = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers=headers,
    )

    segunda = cliente.post(
        "/classify",
        json=MUESTRA_GRAVA,
        headers=headers,
    )

    assert primera.status_code == 200
    assert segunda.status_code == 409
    assert saldo(cuenta) == 9


def test_saldo_cero(cuenta_prueba):
    _, cuenta = cuenta_prueba
    cuenta.update({"creditos": 0})

    respuesta = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers=cabecera(),
    )

    assert respuesta.status_code == 403
    assert saldo(cuenta) == 0
    assert len(list(cuenta.collection(
        "clasificaciones"
    ).stream())) == 0


@pytest.mark.parametrize(
    "cambio",
    [
        {"inorganico_confirmado": False},
        {"pasa_malla_200": 101},
        {"limite_plastico": 300},
        {"pasa_malla_200": True},
        {"dato_desconocido": 1},
    ],
)
def test_rechaza_entrada_invalida(
    cambio,
    cuenta_prueba,
):
    _, cuenta = cuenta_prueba

    respuesta = cliente.post(
        "/classify",
        json={**MUESTRA_FINA, **cambio},
        headers=cabecera(),
    )

    assert respuesta.status_code == 422, respuesta.text
    assert saldo(cuenta) == 10


def test_rechaza_sin_clave_operacion(cuenta_prueba):
    _, cuenta = cuenta_prueba

    respuesta = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
    )

    assert respuesta.status_code == 422
    assert saldo(cuenta) == 10


def test_rechaza_sin_token():
    respuesta = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers=cabecera(),
    )

    assert respuesta.status_code == 401
    assert (
        respuesta.headers["www-authenticate"]
        == "Bearer"
    )


def test_rechaza_token_invalido(monkeypatch):
    monkeypatch.setenv(
        "FIREBASE_AUTH_EMULATOR_HOST",
        "127.0.0.1:9099",
    )

    respuesta = cliente.post(
        "/classify",
        json=MUESTRA_FINA,
        headers={
            **cabecera(),
            "Authorization": "Bearer token-invalido",
        },
    )

    assert respuesta.status_code == 401