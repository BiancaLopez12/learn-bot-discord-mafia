from dataclasses import dataclass
from time import time
from random import Random

from juego.rol import Detective, Doctor, Ciudadano, Asesino, Rol


def asignar_rol_aleatorio() -> Rol:
    dados = Random()
    dados.seed(time())
    dados = dados.randint(0, 9)
    if dados in range(0, 2):
        return Detective()
    if dados in range(2, 4):
        return Doctor()
    if dados in range(4, 6):
        return Asesino()
    return Ciudadano()
