from dataclasses import dataclass
from juego.partida import Partida
from discord import User, Member


@dataclass
class Mafia:
    partida_en_curso = Partida()

    def crear_partida(self, cantidad_de_jugadores: int):
        self.partida_en_curso = Partida(cantidad_de_jugadores)
        return self

    def agregar_jugador(self, jugador: User | Member):
        self.partida_en_curso.agregar_jugador_si_es_posible(jugador)
        return self

    async def comenzar(self):
        self.partida_en_curso.completar_partida_si_es_necesario()
        self.partida_en_curso.asignar_roles()
        await self.partida_en_curso.comunicar_roles_por_mp()
        return self
