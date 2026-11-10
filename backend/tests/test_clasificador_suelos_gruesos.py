
import pytest

from app.domain.muestra_suelo import MuestraSuelo
from app.domain.clasificador_suelos_gruesos import (
    clasificar_suelo_grueso,
)


def crear_muestra(
        p4,
        p200,
        ll=None,
        lp=None,
        d10=None,
        d30=None,
        d60=None,
):
    return MuestraSuelo(
        identificador="M-PRUEBA-GRUESOS",
        pasa_malla_4=p4,
        pasa_malla_200=p200,
        limite_liquido=ll,
        limite_plastico=lp,
        d10=d10,
        d30=d30,
        d60=d60,
    )


def clasificar(muestra):
    return clasificar_suelo_grueso(
        muestra,
        inorganico_confirmado=True,
    )


def test_grava_bien_graduada_gw():
    m = crear_muestra(
        30, 2,
        d10=0.1, d30=0.3, d60=0.6,
    )
    assert clasificar(m).simbolo == "GW"


def test_grava_mal_graduada_gp():
    m = crear_muestra(
        30, 2,
        d10=0.1, d30=0.2, d60=0.3,
    )
    assert clasificar(m).simbolo == "GP"


def test_arena_bien_graduada_sw():
    m = crear_muestra(
        90, 2,
        d10=0.1, d30=0.3, d60=0.6,
    )
    assert clasificar(m).simbolo == "SW"


def test_arena_mal_graduada_sp():
    m = crear_muestra(
        90, 2,
        d10=0.1, d30=0.2, d60=0.3,
    )
    assert clasificar(m).simbolo == "SP"


def test_grava_limosa_gm():
    m = crear_muestra(
        35, 20,
        ll=35, lp=30,
    )
    assert clasificar(m).simbolo == "GM"


def test_grava_arcillosa_gc():
    m = crear_muestra(
        35, 20,
        ll=40, lp=20,
    )
    assert clasificar(m).simbolo == "GC"


def test_arena_limosa_sm():
    m = crear_muestra(
        85, 20,
        ll=35, lp=30,
    )
    assert clasificar(m).simbolo == "SM"


def test_arena_arcillosa_sc():
    m = crear_muestra(
        85, 20,
        ll=40, lp=20,
    )
    assert clasificar(m).simbolo == "SC"


def test_simbolo_doble_gw_gm():
    m = crear_muestra(
        30, 8,
        ll=35, lp=30,
        d10=0.1, d30=0.3, d60=0.6,
    )
    assert clasificar(m).simbolo == "GW-GM"


def test_simbolo_doble_sp_sc():
    m = crear_muestra(
        90, 8,
        ll=40, lp=20,
        d10=0.1, d30=0.2, d60=0.3,
    )
    assert clasificar(m).simbolo == "SP-SC"


def test_finos_exactamente_5():
    m = crear_muestra(
        30, 5,
        ll=35, lp=30,
        d10=0.1, d30=0.3, d60=0.6,
    )
    assert clasificar(m).simbolo == "GW-GM"


def test_finos_exactamente_12():
    m = crear_muestra(
        90, 12,
        ll=40, lp=20,
        d10=0.1, d30=0.2, d60=0.3,
    )
    assert clasificar(m).simbolo == "SP-SC"


def test_finos_fronterizos_grava():
    m = crear_muestra(
        35, 20,
        ll=25, lp=19,
    )
    assert clasificar(m).simbolo == "GC-GM"


def test_finos_fronterizos_arena():
    m = crear_muestra(
        85, 20,
        ll=25, lp=19,
    )
    assert clasificar(m).simbolo == "SC-SM"


def test_rechaza_falta_diametros():
    m = crear_muestra(30, 2)

    with pytest.raises(ValueError):
        clasificar(m)


def test_rechaza_suelo_fino():
    m = crear_muestra(90, 70)

    with pytest.raises(ValueError):
        clasificar(m)


def test_requiere_confirmacion_inorganico():
    m = crear_muestra(
        90, 2,
        d10=0.1, d30=0.3, d60=0.6,
    )

    with pytest.raises(ValueError):
        clasificar_suelo_grueso(m)


def test_igualdad_grava_arena():
    # Grava: 100 - 55 = 45 %
    # Arena: 55 - 10 = 45 %
    # La igualdad se clasifica como arena.
    m = crear_muestra(
        55, 10,
        ll=40, lp=20,
        d10=0.1, d30=0.3, d60=0.6,
    )

    resultado = clasificar(m)

    assert resultado.tipo == "arena"
    assert resultado.simbolo == "SW-SC"
