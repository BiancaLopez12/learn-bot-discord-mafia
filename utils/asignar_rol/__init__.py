from time import time
from random import Random

from juego.rol import Detective, Doctor, Ciudadano, Asesino, Rol


def asignar_rol_aleatorio(cantidad_de_asesinos: int) -> Rol:
    dados = Random()
    dados.seed(time())
    probabilidad_de_que_sea_doctor = (2 * cantidad_de_asesinos) * 5  # 0, 10, 20
    probabilidad_de_que_sea_detective = (2 * cantidad_de_asesinos) * 5  # 0, 10, 20
    probabilidad_de_que_sea_ciudadano = (2 * cantidad_de_asesinos) * 10  # 0, 20, 40
    dados = dados.randint(0, 100)
    if dados in range(0, probabilidad_de_que_sea_ciudadano):
        return Ciudadano()
    if dados in range(
        probabilidad_de_que_sea_ciudadano,
        probabilidad_de_que_sea_ciudadano + probabilidad_de_que_sea_doctor,
    ):
        return Doctor()
    if dados in range(
        probabilidad_de_que_sea_ciudadano + probabilidad_de_que_sea_doctor,
        probabilidad_de_que_sea_ciudadano
        + probabilidad_de_que_sea_doctor
        + probabilidad_de_que_sea_detective,
    ):
        return Detective()
    return Asesino()
