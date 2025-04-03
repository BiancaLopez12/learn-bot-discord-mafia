from dataclasses import dataclass
from discord import User, Member
from random import Random
from time import time
from juego.rol import Rol
from utils.asignar_rol import asignar_rol_aleatorio


@dataclass
class Jugador(Random):
    rol = Rol()

    def __init__(self):
        self.seed(time())
        super().__init__()

    def seleccionar_rol(self):
        self.rol = asignar_rol_aleatorio()

    async def comunicar_rol_al_usuario(self):
        return self


@dataclass
class JugadorReal(Jugador):
    usuario: User | Member

    async def comunicar_rol_al_usuario(self):
        await self.usuario.send(f"Tu rol es: {self.rol}")
        return self


@dataclass
class JugadorNPC(Jugador):
    pass
