
from dataclasses import dataclass
from math import isclose
from typing import Optional, Tuple

from app.domain.muestra_suelo import MuestraSuelo


@dataclass(frozen=True)
class ResultadoSueloGrueso:
    """Resultado preliminar de clasificación SUCS."""

    simbolo: str
    descripcion: str
    tipo: str
    porcentaje_finos: float
    coeficiente_uniformidad: Optional[float]
    coeficiente_curvatura: Optional[float]
    advertencias: Tuple[str, ...] = ()


def _determinar_tipo(muestra: MuestraSuelo) -> str:
    """
    Determina si predomina grava o arena
    dentro de la fracción gruesa.
    """

    p4 = muestra.pasa_malla_4
    p200 = muestra.pasa_malla_200

    if p4 is None or p200 is None:
        raise ValueError(
            "Se requieren los porcentajes pasantes "
            "de las mallas No. 4 y No. 200."
        )

    if p200 >= 50:
        raise ValueError(
            "Esta función solamente clasifica "
            "suelos gruesos: P200 < 50 %."
        )

    porcentaje_grava = 100 - p4
    porcentaje_arena = p4 - p200

    if porcentaje_grava > porcentaje_arena:
        return "grava"

    return "arena"


def _determinar_graduacion(
        muestra: MuestraSuelo,
        tipo: str,
) -> str:
    """
    Determina la graduación del suelo.

    W: bien graduado.
    P: mal graduado.

    Utiliza Cu y Cc con tolerancia para
    evitar errores de precisión decimal.
    """

    cu = muestra.coeficiente_uniformidad
    cc = muestra.coeficiente_curvatura

    if cu is None or cc is None:
        raise ValueError(
            "Se necesitan D10, D30 y D60 "
            "para determinar la graduación."
        )

    cu_minimo = 4 if tipo == "grava" else 6

    # Evita errores como:
    # 0.6 / 0.1 = 5.999999999999999
    # cuando matemáticamente es 6.

    cumple_cu = (
            cu > cu_minimo
            or isclose(
        cu,
        cu_minimo,
        rel_tol=1e-12,
    )
    )

    cumple_cc_inferior = (
            cc > 1
            or isclose(
        cc,
        1,
        rel_tol=1e-12,
    )
    )

    cumple_cc_superior = (
            cc < 3
            or isclose(
        cc,
        3,
        rel_tol=1e-12,
    )
    )

    bien_graduado = (
            cumple_cu
            and cumple_cc_inferior
            and cumple_cc_superior
    )

    return "W" if bien_graduado else "P"


def _determinar_naturaleza_finos(
        muestra: MuestraSuelo,
) -> str:
    """
    Determina la naturaleza de los finos
    mediante los límites de Atterberg.

    M: comportamiento limoso.
    C: comportamiento arcilloso.
    MC: comportamiento fronterizo CL-ML.
    """

    ll = muestra.limite_liquido
    ip = muestra.indice_plasticidad
    linea_a = muestra.linea_a

    if ll is None or ip is None or linea_a is None:
        raise ValueError(
            "Se requieren LL y LP "
            "para caracterizar los finos."
        )

    if ip >= linea_a and 4 <= ip <= 7:
        return "MC"

    if ip >= linea_a and ip > 7:
        return "C"

    return "M"


def clasificar_suelo_grueso(
        muestra: MuestraSuelo,
        *,
        inorganico_confirmado: bool = False,
) -> ResultadoSueloGrueso:
    """
    Clasificación SUCS preliminar
    de gravas y arenas.

    Considera:
    - Menos de 5 % de finos.
    - Entre 5 % y 12 % de finos.
    - Más de 12 % de finos.

    Requiere que los datos granulométricos
    correspondan al material considerado
    para la clasificación ASTM D2487.

    No sustituye una revisión normativa
    completa del informe de laboratorio.
    """

    if not inorganico_confirmado:
        raise ValueError(
            "Debe confirmarse que el material "
            "es inorgánico."
        )

    tipo = _determinar_tipo(muestra)

    finos = muestra.pasa_malla_200

    prefijo = "G" if tipo == "grava" else "S"
    nombre = "Grava" if tipo == "grava" else "Arena"

    cu = muestra.coeficiente_uniformidad
    cc = muestra.coeficiente_curvatura

    advertencias = []

    if finos < 5:
        # SUELO GRUESO LIMPIO

        graduacion = _determinar_graduacion(
            muestra,
            tipo,
        )

        simbolo = prefijo + graduacion

        texto_graduacion = (
            "bien graduada"
            if graduacion == "W"
            else "mal graduada"
        )

        descripcion = (
            f"{nombre} {texto_graduacion}"
        )

    elif finos <= 12:
        # SUELO CON 5 A 12 % DE FINOS
        # REQUIERE SIMBOLO DOBLE

        graduacion = _determinar_graduacion(
            muestra,
            tipo,
        )

        naturaleza = _determinar_naturaleza_finos(
            muestra
        )

        primer_simbolo = prefijo + graduacion

        if naturaleza == "MC":
            # Criterio preliminar cuando
            # los finos están en zona CL-ML.

            segundo_simbolo = prefijo + "C"

            advertencias.append(
                "Finos en la zona CL-ML; "
                "revisar la descripción "
                "normativa del símbolo doble."
            )

        else:
            segundo_simbolo = prefijo + naturaleza

        simbolo = (
                primer_simbolo
                + "-"
                + segundo_simbolo
        )

        texto_graduacion = (
            "bien graduada"
            if graduacion == "W"
            else "mal graduada"
        )

        texto_finos = (
            "arcillosos"
            if segundo_simbolo.endswith("C")
            else "limosos"
        )

        descripcion = (
            f"{nombre} {texto_graduacion} "
            f"con finos {texto_finos}"
        )

    else:
        # SUELO CON MAS DE 12 % DE FINOS

        naturaleza = _determinar_naturaleza_finos(
            muestra
        )

        if naturaleza == "MC":
            simbolo = (
                "GC-GM"
                if tipo == "grava"
                else "SC-SM"
            )

            descripcion = (
                f"{nombre} con finos "
                "arcillosos y limosos"
            )

        elif naturaleza == "C":
            simbolo = prefijo + "C"
            descripcion = f"{nombre} arcillosa"

        else:
            simbolo = prefijo + "M"
            descripcion = f"{nombre} limosa"

    # ADVERTENCIA DE LINEA U

    ip = muestra.indice_plasticidad
    linea_u = muestra.linea_u

    if (
            ip is not None
            and linea_u is not None
            and ip > linea_u
    ):
        advertencias.append(
            "El punto está por encima de "
            "la línea U. Revisar los límites "
            "de Atterberg."
        )

    return ResultadoSueloGrueso(
        simbolo=simbolo,
        descripcion=descripcion,
        tipo=tipo,
        porcentaje_finos=finos,
        coeficiente_uniformidad=cu,
        coeficiente_curvatura=cc,
        advertencias=tuple(advertencias),
    )
