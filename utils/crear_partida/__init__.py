import re
from dataclasses import dataclass


def extraer_cantidad_de_jugadores(mensaje: str) -> int:
    try:
        patron = re.compile(r"!crear (?P<cantidad>(\d+))")
        coincidencias = patron.match(mensaje)
        return int(coincidencias["cantidad"])  # type: ignore
    except Exception:
        raise NoSePudoDeterminarCantidadDeJugadores(mensaje)


@dataclass
class NoSePudoDeterminarCantidadDeJugadores(Exception):
    mensaje_con_error: str

    def __str__(self):
        return f"No se pudo extraer la cantidad de jugadores del comando {self.mensaje_con_error}"
