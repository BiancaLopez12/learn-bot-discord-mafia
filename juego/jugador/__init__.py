from dataclasses import dataclass
from discord import User, Member
from juego.rol import Rol
from utils.asignar_rol import asignar_rol_aleatorio


@dataclass
class Jugador:
    rol = Rol()

    def seleccionar_rol(self, cantidad_de_mafiosos: int):
        self.rol = asignar_rol_aleatorio(cantidad_de_mafiosos)

    def es_un_mafioso(self):
        return self.rol.es_un_mafioso()

    async def comunicar_rol_al_usuario(self):
        return self

    async def votar_por_una_victima(self):
        return self


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
