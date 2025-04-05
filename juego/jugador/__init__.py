from dataclasses import dataclass
from discord import User, Member
from juego.rol import Rol
from utils.asignar_rol import asignar_rol_aleatorio


@dataclass
class Jugador:
    rol = Rol()

    def seleccionar_rol(self, cantidad_de_asesinos: int):
        self.rol = asignar_rol_aleatorio(cantidad_de_asesinos)

    def es_un_asesino(self):
        return self.rol.soy_un_asesino()

    async def comunicar_rol_al_usuario(self):
        return self

    async def quien_sera_tu_victima(self):
        return self


@dataclass
class JugadorReal(Jugador):
    usuario: User | Member

    async def comunicar_rol_al_usuario(self):
        await self.usuario.send(f"Tu rol es: {self.rol}")
        return self

    async def quien_sera_tu_victima(self):
        await self.rol.quien_sera_tu_victima(self.usuario)
        return self


@dataclass
class JugadorNPC(Jugador):
    pass
