
from dataclasses import dataclass
from math import isfinite
from typing import Optional


@dataclass(frozen=True)
class MuestraSuelo:
    """Datos de laboratorio de una muestra de suelo."""

    identificador: str
    limite_liquido: Optional[float] = None
    limite_plastico: Optional[float] = None

    pasa_malla_4: Optional[float] = None
    pasa_malla_40: Optional[float] = None
    pasa_malla_200: Optional[float] = None

    d10: Optional[float] = None
    d30: Optional[float] = None
    d60: Optional[float] = None

    def __post_init__(self):
        if not self.identificador or not self.identificador.strip():
            raise ValueError(
                "La muestra debe tener un identificador."
            )

        campos_porcentaje = {
            "pasa_malla_4": self.pasa_malla_4,
            "pasa_malla_40": self.pasa_malla_40,
            "pasa_malla_200": self.pasa_malla_200,
        }

        for nombre, valor in campos_porcentaje.items():
            if valor is not None:
                self._validar_numero(nombre, valor)
                if not 0 <= valor <= 100:
                    raise ValueError(
                        f"{nombre} debe estar entre 0 y 100."
                    )

        tamices = [
            self.pasa_malla_4,
            self.pasa_malla_40,
            self.pasa_malla_200,
        ]

        # Un tamiz más fino no puede registrar mayor
        # porcentaje pasante que uno más grueso.
        for anterior, siguiente in zip(tamices, tamices[1:]):
            if (
                anterior is not None
                and siguiente is not None
                and anterior < siguiente
            ):
                raise ValueError(
                    "Los porcentajes pasantes deben cumplir "
                    "P4 >= P40 >= P200."
                )

        for nombre, valor in {
            "limite_liquido": self.limite_liquido,
            "limite_plastico": self.limite_plastico,
        }.items():
            if valor is not None:
                self._validar_numero(nombre, valor)
                if valor < 0:
                    raise ValueError(
                        f"{nombre} no puede ser negativo."
                    )

        if (
            self.limite_liquido is not None
            and self.limite_plastico is not None
            and self.limite_plastico > self.limite_liquido
        ):
            raise ValueError(
                "El límite plástico no puede superar "
                "el límite líquido."
            )

        diametros = {
            "d10": self.d10,
            "d30": self.d30,
            "d60": self.d60,
        }

        presentes = [
            valor is not None
            for valor in diametros.values()
        ]

        if any(presentes) and not all(presentes):
            raise ValueError(
                "Para calcular Cu y Cc deben proporcionarse "
                "D10, D30 y D60."
            )

        if all(presentes):
            for nombre, valor in diametros.items():
                self._validar_numero(nombre, valor)
                if valor <= 0:
                    raise ValueError(
                        f"{nombre} debe ser mayor que cero."
                    )

            if not self.d10 <= self.d30 <= self.d60:
                raise ValueError(
                    "Los diámetros deben cumplir "
                    "D10 <= D30 <= D60."
                )

    @staticmethod
    def _validar_numero(nombre: str, valor: float):
        if isinstance(valor, bool) or not isinstance(
            valor, (int, float)
        ):
            raise ValueError(
                f"{nombre} debe ser un número."
            )

        if not isfinite(valor):
            raise ValueError(
                f"{nombre} debe ser un número finito."
            )

    @property
    def indice_plasticidad(self) -> Optional[float]:
        if (
            self.limite_liquido is None
            or self.limite_plastico is None
        ):
            return None

        return (
            self.limite_liquido - self.limite_plastico
        )

    @property
    def linea_a(self) -> Optional[float]:
        if self.limite_liquido is None:
            return None

        return 0.73 * (self.limite_liquido - 20)

    @property
    def linea_u(self) -> Optional[float]:
        if self.limite_liquido is None:
            return None

        return 0.9 * (self.limite_liquido - 8)

    @property
    def coeficiente_uniformidad(self) -> Optional[float]:
        if self.d10 is None or self.d60 is None:
            return None

        return self.d60 / self.d10

    @property
    def coeficiente_curvatura(self) -> Optional[float]:
        if (
            self.d10 is None
            or self.d30 is None
            or self.d60 is None
        ):
            return None

        return (self.d30 ** 2) / (self.d10 * self.d60)
