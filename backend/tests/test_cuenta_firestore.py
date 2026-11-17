import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

import pytest
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore

from app.api.cuenta import crear_cuenta_si_falta


@pytest.fixture
def cuenta_local():
    if os.environ.get("FIRESTORE_EMULATOR_HOST") != "127.0.0.1:8080":
        pytest.skip("Requiere Firestore local en 127.0.0.1:8080")

    cliente = firestore.Client(
        project="demo-sucs-local",
        credentials=AnonymousCredentials(),
    )
    referencia = cliente.collection("usuarios").document(
        f"test-cuenta-{uuid4().hex}"
    )

    try:
        yield cliente, referencia
    finally:
        referencia.delete(timeout=10)
        cliente.close()


def test_crea_cuenta_con_diez_creditos(cuenta_local):
    cliente, referencia = cuenta_local

    resultado = crear_cuenta_si_falta(
        cliente.transaction(),
        referencia,
    )
    guardado = referencia.get(timeout=10).to_dict()

    assert resultado["creditos"] == 10
    assert guardado["creditos"] == 10
    assert guardado["bienvenida_otorgada"] is True
    assert guardado["creado_en"] is not None


def test_inicializar_conserva_saldo_existente(cuenta_local):
    cliente, referencia = cuenta_local
    crear_cuenta_si_falta(cliente.transaction(), referencia)
    referencia.update({"creditos": 7}, timeout=10)
    antes = referencia.get(timeout=10).to_dict()

    resultado = crear_cuenta_si_falta(
        cliente.transaction(),
        referencia,
    )
    despues = referencia.get(timeout=10).to_dict()

    assert resultado["creditos"] == 7
    assert despues == antes


def test_inicializaciones_simultaneas(cuenta_local):
    cliente, referencia = cuenta_local
    barrera = Barrier(2)

    def inicializar():
        barrera.wait(timeout=10)
        return crear_cuenta_si_falta(
            cliente.transaction(max_attempts=5),
            referencia,
        )

    with ThreadPoolExecutor(max_workers=2) as ejecutor:
        primera = ejecutor.submit(inicializar)
        segunda = ejecutor.submit(inicializar)
        resultados = [primera.result(), segunda.result()]

    assert [resultado["creditos"] for resultado in resultados] == [10, 10]

    guardado = referencia.get(timeout=10).to_dict()
    assert guardado["creditos"] == 10
    assert guardado["bienvenida_otorgada"] is True