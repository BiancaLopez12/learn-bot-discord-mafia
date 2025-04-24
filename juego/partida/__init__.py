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
        self.cantidad_de_mafiosos = 0

    def determinar_cantidad_de_mafiosos(self):
        return self.cantidad_de_mafiosos
    
    def determinar_cantidad_de_jugadores(self):
        return self.cantidad_de_ciudadanos + self.cantidad_de_mafiosos
    

    def expulsar_al_jugador(self, nick_del_jugador_expulsado:str):
        jugador = self.jugadores_mapeados_por_nick.pop(nick_del_jugador_expulsado)  
        if jugador.es_un_mafioso():
            self.cantidad_de_mafiosos -= 1
        else:
            self.cantidad_de_ciudadanos -= 1
        return jugador

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
            jugador.seleccionar_rol(self.cantidad_de_mafiosos)
            if jugador.es_un_mafioso():
                self.cantidad_de_mafiosos += 1
            if not jugador.es_un_mafioso():
                self.cantidad_de_ciudadanos += 1
        return self
    


    async def comunicar_roles_por_mp(self):
        avisos = [
            jugador.comunicar_rol_al_usuario()
            for jugador in self.jugadores_mapeados_por_nick.values()
        ]
        await asyncio.gather(*avisos)
        return self

    async def consultar_a_los_mafiosos_a_quien_van_a_matar(self):
        avisos = [
            jugador.votar_por_una_victima()
            for jugador in self.jugadores_mapeados_por_nick.values()
        ]
        await asyncio.gather(*avisos)
        return self

    def hay_un_equipo_ganador(self):
        return (
            self.cantidad_de_mafiosos >= self.cantidad_de_ciudadanos
            or self.cantidad_de_mafiosos == 0
        )

    def quitar_al_jugador_elegido_por_los_mafiosos(self, nick: str):
        self.jugadores_mapeados_por_nick.pop(nick)
        self.cantidad_de_ciudadanos -= 1

        return self

    async def informar_el_equipo_ganador(self, contexto: commands.Context):
        if not self.hay_un_equipo_ganador():
            await contexto.send("No hay un equipo ganador.")

        ganaron_los_mafiosos = self.cantidad_de_mafiosos >= self.cantidad_de_ciudadanos
        if ganaron_los_mafiosos:
            await contexto.send("Ganaron los mafiosos!")

        ganaron_los_ciudadanos = self.cantidad_de_mafiosos == 0
        if ganaron_los_ciudadanos:
            await contexto.send("Ganaron los ciudadanos!")

        return self

    def verificar_si_el_mafioso_esta_en_juego(self, nick_del_mafioso: str):
        mafioso = self.jugadores_mapeados_por_nick.get(nick_del_mafioso)
        if not mafioso:
            raise Exception(f"{nick_del_mafioso} no está en la partida.")
        if not mafioso.es_un_mafioso():
            raise Exception(f"{nick_del_mafioso} no es un mafioso.")
        return self

    def verificar_si_la_victima_esta_en_juego(self, nick_de_la_victima: str):
        victima = self.jugadores_mapeados_por_nick.get(nick_de_la_victima)
        if not victima:
            raise Exception(f"{nick_de_la_victima} no está en la partida.")
        if victima.es_un_mafioso():
            raise Exception(f"{nick_de_la_victima} es un mafioso.")
        return self

    async def informar_configuracion(self, contexto: commands.Context):
        await contexto.send(
            f"Configuración de la partida:\n"
            f"Jugadores: {len(self.jugadores_mapeados_por_nick)}\n"
            f"Mafiosos: {self.cantidad_de_mafiosos}\n"
            f"Ciudadanos: {self.cantidad_de_ciudadanos}"
        )
        return self
