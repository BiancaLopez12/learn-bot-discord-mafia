from time import time
from random import Random

from juego.rol import Detective, Doctor, Ciudadano, Asesino, Rol


def asignar_rol_aleatorio() -> Rol:
    dados = Random()
    dados.seed(time())
    dados = dados.randint(0, 100)
    if dados in range(0, 20):
        return Detective()
    if dados in range(20, 40):
        return Doctor()
    if dados in range(40, 60):
        return Asesino()
    return Ciudadano()
