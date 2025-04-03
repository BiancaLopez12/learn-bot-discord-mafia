import re
from dataclasses import dataclass


def extraer_nick_de_la_victima(mensaje: str) -> str:
    try:
        patron = re.compile(r"!matar (?P<victima>([a-zA-Z]+))")
        coincidencias = patron.match(mensaje)
        return coincidencias["victima"]  # type: ignore
    except Exception:
        raise NoSePudoDeterminarLaVictima(mensaje)


@dataclass
class NoSePudoDeterminarLaVictima(Exception):
    mensaje_con_error: str

    def __str__(self):
        return f"No se pudo extraer el nick de la victima del comando {self.mensaje_con_error}"
