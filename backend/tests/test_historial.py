"""Pruebas de historial privado con Firestore Emulator."""

import os
from hashlib import sha256
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore

from app.api.autenticacion import obtener_usuario_actual
from app.base_datos import obtener_base_datos
from app.main import app


cliente = TestClient(app)


@pytest.fixture
def entorno():
    assert os.environ.get(
        "FIRESTORE_EMULATOR_HOST"
    ) == "127.0.0.1:8080"

    db = firestore.Client(
        project="demo-sucs-local",
        credentials=AnonymousCredentials(),
    )

    uid = f"historial-{uuid4().hex}"
    otro_uid = f"otro-{uuid4().hex}"

    cuenta = db.collection("usuarios").document(uid)
    otra_cuenta = db.collection("usuarios").document(otro_uid)

    cuenta.set({"creditos": 10})
    otra_cuenta.set({"creditos": 10})

    app.dependency_overrides[obtener_usuario_actual] = (
        lambda: {"uid": uid}
    )
    app.dependency_overrides[obtener_base_datos] = (
        lambda: db
    )

    def crear(usuario_id, nombre):
        identificador = sha256(
            nombre.encode("utf-8")
        ).hexdigest()

        referencia = (
            db.collection("usuarios")
            .document(usuario_id)
            .collection("clasificaciones")
            .document(identificador)
        )

        referencia.set({
            "entrada": {"identificador": nombre},
            "resultado": {"simbolo": "CL"},
            "creditos_consumidos": 1,
            "creado_en": firestore.SERVER_TIMESTAMP,
        })

        return identificador

    try:
        yield db, uid, otro_uid, crear

    finally:
        app.dependency_overrides.clear()

        for usuario_id in (uid, otro_uid):
            referencia = db.collection(
                "usuarios"
            ).document(usuario_id)

            for doc in referencia.collection(
                "clasificaciones"
            ).stream():
                doc.reference.delete()

            referencia.delete()

        db.close()


def test_historial_vacio(entorno):
    respuesta = cliente.get("/classifications")

    assert respuesta.status_code == 200
    assert respuesta.json()["elementos"] == []
    assert respuesta.json()["hay_mas"] is False


def test_listar_no_descuenta_creditos(entorno):
    db, uid, _, crear = entorno

    crear(uid, "MUESTRA-A")
    crear(uid, "MUESTRA-B")

    respuesta = cliente.get("/classifications")

    assert respuesta.status_code == 200
    assert len(respuesta.json()["elementos"]) == 2

    saldo = db.collection("usuarios").document(
        uid
    ).get().to_dict()["creditos"]

    assert saldo == 10


def test_detalle_gratuito(entorno):
    db, uid, _, crear = entorno

    identificador = crear(uid, "MUESTRA-C")

    respuesta = cliente.get(
        f"/classifications/{identificador}"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == identificador
    assert respuesta.json()["resultado"]["simbolo"] == "CL"

    cuenta = db.collection("usuarios").document(uid)
    assert cuenta.get().to_dict()["creditos"] == 10


def test_aislamiento_entre_usuarios(entorno):
    _, _, otro_uid, crear = entorno

    identificador = crear(
        otro_uid, "MUESTRA-PRIVADA"
    )

    listado = cliente.get("/classifications")
    detalle = cliente.get(
        f"/classifications/{identificador}"
    )

    assert listado.status_code == 200
    assert listado.json()["elementos"] == []
    assert detalle.status_code == 404


def test_paginacion(entorno):
    _, uid, _, crear = entorno

    for numero in range(5):
        crear(uid, f"MUESTRA-{numero}")

    primera = cliente.get(
        "/classifications",
        params={"limite": 2},
    )

    assert primera.status_code == 200
    datos = primera.json()
    assert len(datos["elementos"]) == 2
    assert datos["hay_mas"] is True
    assert datos["siguiente_cursor"] is not None

    segunda = cliente.get(
        "/classifications",
        params={
            "limite": 2,
            "cursor": datos["siguiente_cursor"],
        },
    )

    assert segunda.status_code == 200
    assert len(segunda.json()["elementos"]) == 2

    ids_primera = {
        item["id"] for item in datos["elementos"]
    }
    ids_segunda = {
        item["id"]
        for item in segunda.json()["elementos"]
    }

    assert ids_primera.isdisjoint(ids_segunda)


def test_cursor_ajeno_rechazado(entorno):
    _, _, otro_uid, crear = entorno

    identificador = crear(otro_uid, "AJENA")

    respuesta = cliente.get(
        "/classifications",
        params={"cursor": identificador},
    )

    assert respuesta.status_code == 400


def test_identificador_invalido(entorno):
    respuesta = cliente.get(
        "/classifications/id-invalido"
    )

    assert respuesta.status_code == 422


def test_limite_invalido(entorno):
    respuesta = cliente.get(
        "/classifications",
        params={"limite": 1000},
    )

    assert respuesta.status_code == 422


def test_historial_sin_autenticacion():
    respuesta = cliente.get("/classifications")

    assert respuesta.status_code == 401


def test_detalle_sin_autenticacion():
    identificador = "a" * 64

    respuesta = cliente.get(
        f"/classifications/{identificador}"
    )

    assert respuesta.status_code == 401