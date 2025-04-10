from dataclasses import dataclass
from discord import User, Member
from juego.rol import Rol, Ciudadano, Doctor, Detective, Mafioso

# from utils.asignar_rol import asignar_rol_aleatorio
from random import Random
from time import time


@dataclass
class Jugador:
    rol = Rol()

    def seleccionar_rol(self, cantidad_de_mafiosos: int):
        self.rol = self.asignar_rol_aleatorio(cantidad_de_mafiosos)

    def es_un_mafioso(self):
        return self.rol.es_un_mafioso()

    async def comunicar_rol_al_usuario(self):
        return self

    async def votar_por_una_victima(self):
        return self

    def asignar_rol_aleatorio(self, cantidad_de_mafiosos: int) -> Rol:
        dados = Random()
        dados.seed(time())
        probabilidad_de_que_sea_doctor = (2 * cantidad_de_mafiosos) * 5  # 0, 10, 20
        probabilidad_de_que_sea_detective = (2 * cantidad_de_mafiosos) * 5  # 0, 10, 20
        probabilidad_de_que_sea_ciudadano = (2 * cantidad_de_mafiosos) * 10  # 0, 20, 40
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
        return Mafioso()


@dataclass
class JugadorReal(Jugador):
    usuario: User | Member

    async def comunicar_rol_al_usuario(self):
        await self.usuario.send(f"Tu rol es: {self.rol}")
        return self

    async def votar_por_una_victima(self):
        await self.rol.votar_por_una_victima(self.usuario)
        return self


@dataclass
class JugadorNPC(Jugador):
    pass
