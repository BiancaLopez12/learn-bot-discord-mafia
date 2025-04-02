import re
from dataclasses import dataclass


@dataclass
class ErrorAlCrearPartida(Exception):
    mensaje_con_error: str

    def __init__(self, mensaje_con_error: str):
        self.mensaje_con_error = mensaje_con_error

    def __str__(self):
        return f"No se pudo extraer la cantidad de jugadores del comando {self.mensaje_con_error}"


def extraer_cantidad_de_jugadores(mensaje: str) -> int:
    try:
        patron = re.compile(r"!crear (?P<cantidad>(\d+))")
        coincidencias = patron.match(mensaje)
        return int(coincidencias["cantidad"])  # type: ignore
    except Exception:
        raise ErrorAlCrearPartida(mensaje)
