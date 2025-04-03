from dataclasses import dataclass
from juego.etapa import Noche
from juego.partida import Partida
from discord import User, Member
from discord.ext import commands


@dataclass
class Mafia:
    partida_en_curso = Partida()
    etapa = Noche()

    def crear_partida(self, cantidad_de_jugadores: int):
        self.partida_en_curso = Partida(cantidad_de_jugadores)
        return self

    def agregar_jugador(self, jugador: User | Member):
        self.partida_en_curso.agregar_jugador_si_es_posible(jugador)
        return self

    async def asignar_roles_a_los_jugadores(self):
        self.partida_en_curso.completar_partida_si_es_necesario()
        self.partida_en_curso.asignar_roles()
        await self.partida_en_curso.comunicar_roles_por_mp()
        return self

    def hay_un_equipo_ganador(self):
        return self.partida_en_curso.hay_un_equipo_ganador()

    async def actuar_conforme_a_la_etapa_en_curso(self, contexto: commands.Context):
        await self.etapa.actuar(partida=self.partida_en_curso, contexto=contexto)

    def cambiar_de_etapa(self):
        self.etapa = self.etapa.proxima_etapa()
        return self

    async def informar_sobre_lo_ocurrido(self, contexto: commands.Context):
        await self.etapa.informar_sobre_lo_ocurrido(contexto)
        return self

    async def informar_el_equipo_ganador(self, contexto: commands.Context):
        await self.partida_en_curso.informar_el_equipo_ganador(contexto)
        return self

    async def un_asesino_esta_detras_de_alguien(
        self, nick_del_asesino: str, nick_de_la_victima: str
    ):
        await self.etapa.un_asesino_esta_detras_de_alguien(
            nick_del_asesino, nick_de_la_victima, partida=self.partida_en_curso
        )
        return self
