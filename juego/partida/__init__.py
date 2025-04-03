from dataclasses import dataclass
from discord import User, Member
from juego.jugador import Jugador, JugadorNPC, JugadorReal
from discord.ext import commands
import asyncio


class LaPartidaYaEstaCompletaYNoAceptaMasJugadores(Exception):
    def __str__(self):
        return "La partida ya está completa y no acepta más jugadores."


@dataclass
class Partida:
    def __init__(self, cantidad_de_jugadores: int = 0):
        self.cantidad_de_jugadores_requerida = cantidad_de_jugadores
        self.jugadores_mapeados_por_nick: dict[str, Jugador] = {}
        self.cantidad_de_ciudadanos = 0
        self.cantidad_de_asesinos = 0

    def determinar_cantidad_de_asesinos(self):
        return self.cantidad_de_asesinos

    def agregar_jugador_si_es_posible(self, jugador: User | Member):
        self.jugadores_mapeados_por_nick[jugador.name] = JugadorReal(usuario=jugador)
        return self

    def completar_partida_si_es_necesario(self):
        for i in range(
            len(self.jugadores_mapeados_por_nick), self.cantidad_de_jugadores_requerida
        ):
            nick_generico = f"NPC_{i}"
            self.jugadores_mapeados_por_nick[nick_generico] = JugadorNPC()
        return self

    def asignar_roles(self):
        for jugador in self.jugadores_mapeados_por_nick.values():
            jugador.seleccionar_rol()
            self.cantidad_de_asesinos += 1 if jugador.es_un_asesino() else 0
            self.cantidad_de_ciudadanos += 1 if not jugador.es_un_asesino() else 0
        return self

    async def comunicar_roles_por_mp(self):
        avisos = [
            jugador.comunicar_rol_al_usuario()
            for jugador in self.jugadores_mapeados_por_nick.values()
        ]
        await asyncio.gather(*avisos)
        return self

    async def consultar_a_los_asesinos_a_quien_van_a_matar(self):
        avisos = [
            jugador.quien_sera_tu_victima()
            for jugador in self.jugadores_mapeados_por_nick.values()
            if jugador.es_un_asesino()
        ]
        await asyncio.gather(*avisos)
        return self

    def hay_un_equipo_ganador(self):
        return (
            self.cantidad_de_asesinos >= self.cantidad_de_ciudadanos
            or self.cantidad_de_asesinos == 0
        )

    def quitar_al_jugador_elegido_por_los_asesinos(self, nick: str):
        self.jugadores_mapeados_por_nick.pop(nick)
        self.cantidad_de_ciudadanos -= 1

        return self

    async def informar_el_equipo_ganador(self, contexto: commands.Context):
        if not self.hay_un_equipo_ganador():
            await contexto.send("No hay un equipo ganador.")

        ganaron_los_asesinos = self.cantidad_de_asesinos >= self.cantidad_de_ciudadanos
        if ganaron_los_asesinos:
            await contexto.send("Ganaron los asesinos!")

        ganaron_los_ciudadanos = self.cantidad_de_asesinos == 0
        if ganaron_los_ciudadanos:
            await contexto.send("Ganaron los ciudadanos!")

        return self

    def verificar_si_el_asesino_esta_en_juego(self, nick_del_asesino: str):
        asesino = self.jugadores_mapeados_por_nick.get(nick_del_asesino)
        if not asesino:
            raise Exception(f"{nick_del_asesino} no está en la partida.")
        if not asesino.es_un_asesino():
            raise Exception(f"{nick_del_asesino} no es un asesino.")
        return self

    def verificar_si_la_victima_esta_en_juego(self, nick_de_la_victima: str):
        victima = self.jugadores_mapeados_por_nick.get(nick_de_la_victima)
        if not victima:
            raise Exception(f"{nick_de_la_victima} no está en la partida.")
        if victima.es_un_asesino():
            raise Exception(f"{nick_de_la_victima} es un asesino.")
        return self
