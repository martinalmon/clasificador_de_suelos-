
from dataclasses import dataclass
from typing import Tuple

from app.domain.muestra_suelo import MuestraSuelo

from app.domain.clasificador_sucs import (
    clasificar_suelo_fino,
)

from app.domain.clasificador_suelos_gruesos import (
    clasificar_suelo_grueso,
)


@dataclass(frozen=True)
class ResultadoClasificacion:
    """Resultado unificado de clasificación SUCS."""

    identificador: str
    simbolo: str
    descripcion: str
    tipo_suelo: str
    porcentaje_finos: float
    indice_plasticidad: float | None
    advertencias: Tuple[str, ...]


def clasificar_sucs(
        muestra: MuestraSuelo,
        *,
        inorganico_confirmado: bool = False,
) -> ResultadoClasificacion:
    """
    Selecciona automáticamente el clasificador
    SUCS correspondiente.

    Suelos finos: P200 >= 50 %
    Suelos gruesos: P200 < 50 %
    """

    p200 = muestra.pasa_malla_200

    if p200 is None:
        raise ValueError(
            "Se necesita el porcentaje que pasa "
            "la malla No. 200 para clasificar."
        )

    if p200 >= 50:
        resultado = clasificar_suelo_fino(
            muestra,
            inorganico_confirmado=inorganico_confirmado,
        )

        tipo_suelo = "fino"

    else:
        resultado = clasificar_suelo_grueso(
            muestra,
            inorganico_confirmado=inorganico_confirmado,
        )

        tipo_suelo = resultado.tipo

    return ResultadoClasificacion(
        identificador=muestra.identificador,
        simbolo=resultado.simbolo,
        descripcion=resultado.descripcion,
        tipo_suelo=tipo_suelo,
        porcentaje_finos=p200,
        indice_plasticidad=muestra.indice_plasticidad,
        advertencias=resultado.advertencias,
    )
