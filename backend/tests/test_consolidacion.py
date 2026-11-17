"""Pruebas de seguridad, ordenamiento y OpenAPI."""

import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from threading import Barrier
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore

from app.api.autenticacion import obtener_usuario_actual
from app.base_datos import obtener_base_datos
from app.clasificaciones_guardadas import guardar_clasificacion
from app.main import app


@pytest.fixture
def entorno():
    assert os.environ.get(
        "FIRESTORE_EMULATOR_HOST"
    ) == "127.0.0.1:8080"

    db = firestore.Client(
        project="demo-sucs-local",
        credentials=AnonymousCredentials(),
    )

    uid = f"consolidacion-{uuid4().hex}"
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
        yield db, uid, cuenta

    finally:
        app.dependency_overrides.clear()

        for doc in cuenta.collection(
            "clasificaciones"
        ).stream():
            doc.reference.delete()

        cuenta.delete()
        db.close()


def crear_registro(cuenta, nombre, fecha):
    identificador = sha256(
        nombre.encode("utf-8")
    ).hexdigest()

    cuenta.collection("clasificaciones").document(
        identificador
    ).set({
        "entrada": {"identificador": nombre},
        "resultado": {"simbolo": "CL"},
        "creditos_consumidos": 1,
        "creado_en": fecha,
    })

    return identificador


def test_no_hay_doble_gasto_simultaneo(entorno):
    db, uid, cuenta = entorno

    cuenta.update({"creditos": 1})

    barrera = Barrier(2)

    def clasificar(numero):
        barrera.wait(timeout=10)

        try:
            guardar_clasificacion(
                base_datos=db,
                uid=uid,
                clave_operacion=f"operacion-{numero}",
                datos_entrada={
                    "identificador": f"M-{numero}"
                },
                resultado={"simbolo": "CL"},
            )
            return 200

        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(
            executor.map(clasificar, [1, 2])
        )

    assert sorted(resultados) == [200, 403]

    assert cuenta.get().to_dict()["creditos"] == 0

    guardados = list(
        cuenta.collection("clasificaciones").stream()
    )

    assert len(guardados) == 1


def test_historial_ordenado_por_fecha(entorno):
    _, _, cuenta = entorno

    ahora = datetime.now(timezone.utc)

    viejo = crear_registro(
        cuenta, "VIEJO", ahora - timedelta(days=3)
    )

    reciente = crear_registro(
        cuenta, "RECIENTE", ahora
    )

    intermedio = crear_registro(
        cuenta, "INTERMEDIO",
        ahora - timedelta(days=1)
    )

    with TestClient(app) as cliente:
        respuesta = cliente.get("/classifications")

    assert respuesta.status_code == 200, respuesta.text

    identificadores = [
        elemento["id"]
        for elemento in respuesta.json()["elementos"]
    ]

    assert identificadores == [
        reciente, intermedio, viejo
    ]


def test_paginacion_cronologica(entorno):
    _, _, cuenta = entorno

    ahora = datetime.now(timezone.utc)
    esperados = []

    for numero in range(5):
        identificador = crear_registro(
            cuenta,
            f"FECHA-{numero}",
            ahora - timedelta(days=numero),
        )
        esperados.append(identificador)

    with TestClient(app) as cliente:
        primera = cliente.get(
            "/classifications",
            params={"limite": 2},
        )

        assert primera.status_code == 200, primera.text

        pagina_1 = primera.json()

        segunda = cliente.get(
            "/classifications",
            params={
                "limite": 2,
                "cursor": pagina_1["siguiente_cursor"],
            },
        )

        assert segunda.status_code == 200, segunda.text

        pagina_2 = segunda.json()

        tercera = cliente.get(
            "/classifications",
            params={
                "limite": 2,
                "cursor": pagina_2["siguiente_cursor"],
            },
        )

        assert tercera.status_code == 200, tercera.text

    obtenidos = [
        item["id"]
        for pagina in (pagina_1, pagina_2, tercera.json())
        for item in pagina["elementos"]
    ]

    assert obtenidos == esperados
    assert pagina_1["hay_mas"] is True
    assert pagina_2["hay_mas"] is True
    assert tercera.json()["hay_mas"] is False


def test_rutas_registradas_en_swagger():
    esquema = app.openapi()
    rutas = esquema["paths"]

    assert "/classify" in rutas
    assert "/classifications" in rutas
    assert "/classifications/{clasificacion_id}" in rutas

    assert "post" in rutas["/classify"]
    assert "get" in rutas["/classifications"]
    assert "get" in rutas[
        "/classifications/{clasificacion_id}"
    ]

    parametros = rutas["/classify"]["post"].get(
        "parameters", []
    )

    assert any(
        parametro["name"].lower() == "idempotency-key"
        and parametro["in"] == "header"
        and parametro.get("required") is True
        for parametro in parametros
    )