
import pytest

from app.domain.muestra_suelo import MuestraSuelo
from app.domain.clasificador_sucs import clasificar_suelo_fino


def crear_muestra(ll, lp, pasa_200=70):
    return MuestraSuelo(
        identificador="M-PRUEBA",
        limite_liquido=ll,
        limite_plastico=lp,
        pasa_malla_200=pasa_200,
    )


def clasificar(ll, lp, pasa_200=70):
    muestra = crear_muestra(ll, lp, pasa_200)
    return clasificar_suelo_fino(
        muestra,
        inorganico_confirmado=True,
    )


def test_clasifica_ch():
    resultado = clasificar(250, 45)

    assert resultado.simbolo == "CH"
    assert resultado.indice_plasticidad == 205


def test_clasifica_cl():
    resultado = clasificar(40, 20)

    assert resultado.simbolo == "CL"


def test_clasifica_ml():
    resultado = clasificar(35, 30)

    assert resultado.simbolo == "ML"


def test_clasifica_mh():
    resultado = clasificar(70, 45)

    assert resultado.simbolo == "MH"


def test_clasifica_cl_ml():
    resultado = clasificar(25, 19)

    assert resultado.simbolo == "CL-ML"


def test_ll_igual_a_50_es_alta_plasticidad():
    resultado = clasificar(50, 20)

    assert resultado.simbolo == "CH"


def test_rechaza_suelo_grueso():
    muestra = crear_muestra(40, 20, pasa_200=30)

    with pytest.raises(ValueError):
        clasificar_suelo_fino(
            muestra,
            inorganico_confirmado=True,
        )


def test_requiere_confirmar_inorganico():
    muestra = crear_muestra(40, 20)

    with pytest.raises(ValueError):
        clasificar_suelo_fino(muestra)


def test_requiere_limites_atterberg():
    muestra = MuestraSuelo(
        identificador="SIN-LIMITES",
        pasa_malla_200=80,
    )

    with pytest.raises(ValueError):
        clasificar_suelo_fino(
            muestra,
            inorganico_confirmado=True,
        )


def test_advierte_si_supera_linea_u():
    resultado = clasificar(40, 0)

    assert len(resultado.advertencias) == 1
