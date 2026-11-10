
from dataclasses import dataclass
from typing import Tuple

from app.domain.muestra_suelo import MuestraSuelo


@dataclass(frozen=True)
class ResultadoSUCS:
    """Resultado de una clasificación SUCS."""

    simbolo: str
    descripcion: str
    indice_plasticidad: float
    linea_a: float
    advertencias: Tuple[str, ...] = ()


def clasificar_suelo_fino(
        muestra: MuestraSuelo,
        *,
        inorganico_confirmado: bool = False,
) -> ResultadoSUCS:
    """
    Clasifica suelos finos inorgánicos mediante
    los límites de Atterberg.

    Alcance de esta primera versión:
    CL, CH, ML, MH y CL-ML.

    No clasifica todavía suelos orgánicos,
    suelos gruesos ni turbas.
    """

    if muestra.pasa_malla_200 is None:
        raise ValueError(
            "Se necesita el porcentaje que pasa "
            "la malla No. 200."
        )

    if muestra.pasa_malla_200 < 50:
        raise ValueError(
            "Esta función solamente clasifica "
            "suelos con 50 % o más pasando "
            "la malla No. 200."
        )

    if not inorganico_confirmado:
        raise ValueError(
            "Se debe confirmar que el suelo "
            "es inorgánico antes de utilizar "
            "este clasificador."
        )

    ll = muestra.limite_liquido
    ip = muestra.indice_plasticidad
    linea_a = muestra.linea_a
    linea_u = muestra.linea_u

    if ll is None or ip is None or linea_a is None:
        raise ValueError(
            "Se necesitan los límites líquido "
            "y plástico para clasificar."
        )

    # Posición en la carta de plasticidad.
    sobre_linea_a = ip >= linea_a

    # La frontera entre baja y alta
    # plasticidad se encuentra en LL = 50.
    if ll >= 50:
        if sobre_linea_a:
            simbolo = "CH"
            descripcion = (
                "Arcilla inorgánica de alta plasticidad"
            )
        else:
            simbolo = "MH"
            descripcion = (
                "Limo inorgánico de alta plasticidad"
            )

    else:
        # Zona de transición de la carta:
        # IP entre 4 y 7, sobre la línea A.
        if 4 <= ip <= 7 and sobre_linea_a:
            simbolo = "CL-ML"
            descripcion = (
                "Arcilla limosa inorgánica "
                "de baja plasticidad"
            )

        elif ip > 7 and sobre_linea_a:
            simbolo = "CL"
            descripcion = (
                "Arcilla inorgánica de baja plasticidad"
            )

        else:
            simbolo = "ML"
            descripcion = (
                "Limo inorgánico de baja plasticidad"
            )

    advertencias = []

    if linea_u is not None and ip > linea_u:
        advertencias.append(
            "El punto se encuentra por encima "
            "de la línea U. Revisar los datos "
            "de los límites de Atterberg."
        )

    return ResultadoSUCS(
        simbolo=simbolo,
        descripcion=descripcion,
        indice_plasticidad=ip,
        linea_a=linea_a,
        advertencias=tuple(advertencias),
    )
