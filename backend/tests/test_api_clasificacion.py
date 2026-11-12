import pytest
from fastapi.testclient import TestClient

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


def test_clasifica_muestra_fina():
    respuesta = cliente.post("/classify", json=MUESTRA_FINA)

    assert respuesta.status_code == 200, respuesta.text

    resultado = respuesta.json()
    assert resultado["identificador"] == "F-001"
    assert resultado["simbolo"] == "CH"
    assert resultado["tipo_suelo"] == "fino"
    assert resultado["porcentaje_finos"] == 70
    assert resultado["indice_plasticidad"] == 205
    assert isinstance(resultado["advertencias"], list)


def test_clasifica_grava():
    muestra = {
        "identificador": "G-001",
        "pasa_malla_4": 30,
        "pasa_malla_200": 2,
        "d10": 0.1,
        "d30": 0.3,
        "d60": 0.6,
        "inorganico_confirmado": True,
    }

    respuesta = cliente.post("/classify", json=muestra)

    assert respuesta.status_code == 200, respuesta.text

    resultado = respuesta.json()
    assert resultado["identificador"] == "G-001"
    assert resultado["simbolo"] == "GW"
    assert resultado["tipo_suelo"] == "grava"


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
def test_rechaza_entrada_invalida(cambio):
    muestra = {**MUESTRA_FINA, **cambio}

    respuesta = cliente.post("/classify", json=muestra)

    assert respuesta.status_code == 422, respuesta.text
    assert respuesta.json()["detail"]