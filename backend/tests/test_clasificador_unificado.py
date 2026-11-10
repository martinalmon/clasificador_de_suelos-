
import pytest

from app.domain.muestra_suelo import MuestraSuelo
from app.domain.clasificador_unificado import (
    clasificar_sucs,
)


def test_selecciona_suelo_fino():
    muestra = MuestraSuelo(
        identificador="F-001",
        limite_liquido=250,
        limite_plastico=45,
        pasa_malla_4=100,
        pasa_malla_200=70,
    )

    resultado = clasificar_sucs(
        muestra,
        inorganico_confirmado=True,
    )

    assert resultado.simbolo == "CH"
    assert resultado.tipo_suelo == "fino"
    assert resultado.indice_plasticidad == 205


def test_selecciona_grava():
    muestra = MuestraSuelo(
        identificador="G-001",
        pasa_malla_4=30,
        pasa_malla_200=2,
        d10=0.1,
        d30=0.3,
        d60=0.6,
    )

    resultado = clasificar_sucs(
        muestra,
        inorganico_confirmado=True,
    )

    assert resultado.simbolo == "GW"
    assert resultado.tipo_suelo == "grava"


def test_selecciona_arena():
    muestra = MuestraSuelo(
        identificador="S-001",
        pasa_malla_4=90,
        pasa_malla_200=2,
        d10=0.1,
        d30=0.3,
        d60=0.6,
    )

    resultado = clasificar_sucs(
        muestra,
        inorganico_confirmado=True,
    )

    assert resultado.simbolo == "SW"
    assert resultado.tipo_suelo == "arena"


def test_p200_igual_50_es_suelo_fino():
    muestra = MuestraSuelo(
        identificador="F-002",
        limite_liquido=40,
        limite_plastico=20,
        pasa_malla_200=50,
    )

    resultado = clasificar_sucs(
        muestra,
        inorganico_confirmado=True,
    )

    assert resultado.tipo_suelo == "fino"
    assert resultado.simbolo == "CL"


def test_rechaza_muestra_sin_p200():
    muestra = MuestraSuelo(
        identificador="SIN-P200",
    )

    with pytest.raises(ValueError):
        clasificar_sucs(
            muestra,
            inorganico_confirmado=True,
        )


def test_requiere_confirmacion_inorganico():
    muestra = MuestraSuelo(
        identificador="F-003",
        limite_liquido=40,
        limite_plastico=20,
        pasa_malla_200=70,
    )

    with pytest.raises(ValueError):
        clasificar_sucs(muestra)


def test_conserva_identificador():
    muestra = MuestraSuelo(
        identificador="SONDEO-01",
        limite_liquido=40,
        limite_plastico=20,
        pasa_malla_200=70,
    )

    resultado = clasificar_sucs(
        muestra,
        inorganico_confirmado=True,
    )

    assert resultado.identificador == "SONDEO-01"


def test_conserva_advertencias():
    muestra = MuestraSuelo(
        identificador="F-004",
        limite_liquido=40,
        limite_plastico=0,
        pasa_malla_200=70,
    )

    resultado = clasificar_sucs(
        muestra,
        inorganico_confirmado=True,
    )

    assert len(resultado.advertencias) > 0
