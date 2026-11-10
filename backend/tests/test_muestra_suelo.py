
import pytest

from app.domain.muestra_suelo import MuestraSuelo


def test_calculos_de_plasticidad():
    muestra = MuestraSuelo(
        identificador="M-001",
        limite_liquido=250,
        limite_plastico=45,
        pasa_malla_4=100,
        pasa_malla_40=80,
        pasa_malla_200=70,
    )

    assert muestra.indice_plasticidad == 205
    assert muestra.linea_a == pytest.approx(167.9)
    assert muestra.linea_u == pytest.approx(217.8)


def test_coeficientes_granulometricos():
    muestra = MuestraSuelo(
        identificador="M-002",
        d10=0.1,
        d30=0.3,
        d60=0.6,
    )

    assert muestra.coeficiente_uniformidad == pytest.approx(6)
    assert muestra.coeficiente_curvatura == pytest.approx(1.5)


def test_rechaza_porcentaje_fuera_de_rango():
    with pytest.raises(ValueError):
        MuestraSuelo(
            identificador="M-003",
            pasa_malla_200=120,
        )


def test_rechaza_tamices_inconsistentes():
    with pytest.raises(ValueError):
        MuestraSuelo(
            identificador="M-004",
            pasa_malla_4=60,
            pasa_malla_40=80,
            pasa_malla_200=30,
        )


def test_rechaza_limites_inconsistentes():
    with pytest.raises(ValueError):
        MuestraSuelo(
            identificador="M-005",
            limite_liquido=30,
            limite_plastico=45,
        )


def test_rechaza_diametros_incompletos():
    with pytest.raises(ValueError):
        MuestraSuelo(
            identificador="M-006",
            d10=0.1,
            d60=0.6,
        )


def test_permite_muestra_incompleta():
    muestra = MuestraSuelo(
        identificador="M-007",
    )

    assert muestra.indice_plasticidad is None
    assert muestra.coeficiente_uniformidad is None


def test_rechaza_valores_no_finitos():
    with pytest.raises(ValueError):
        MuestraSuelo(
            identificador="M-008",
            limite_liquido=float("nan"),
        )


def test_rechaza_identificador_vacio():
    with pytest.raises(ValueError):
        MuestraSuelo(
            identificador=" ",
        )
