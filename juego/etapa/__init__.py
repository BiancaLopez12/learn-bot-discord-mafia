from dataclasses import dataclass
from juego.partida import Partida
from discord.ext import commands
import asyncio


@dataclass
class Etapa:
    def proxima_etapa(self):
        return Etapa()

    async def actuar(self, partida: Partida, contexto: commands.Context):
        return self

    async def informar_sobre_lo_ocurrido(self, contexto: commands.Context):
        await contexto.send("No hay nada que informar.")

    async def un_asesino_esta_detras_de_alguien(
        self, nick_del_asesino: str, nick_de_la_victima: str, partida: Partida
    ):
        return self


@dataclass
class Dia(Etapa):
    def proxima_etapa(self):
        return Noche()

    async def actuar(self, partida: Partida, contexto: commands.Context):
        return self


@dataclass
class Noche(Etapa):
    def __init__(self):
        self.cantidad_de_segundos_a_esperar = 10
        self.cantidad_de_asesinos_que_votan = 0
        self.votacion_en_proceso = asyncio.Lock()
        self.urna_con_posibles_victimas: dict[str, int] = {}

    def proxima_etapa(self):
        return Dia()

    async def actuar(self, partida: Partida, contexto: commands.Context):
        await partida.consultar_a_los_asesinos_a_quien_van_a_matar()
        self.cantidad_de_asesinos_que_votan = partida.determinar_cantidad_de_asesinos()
        while (
            not await self.asesinos_hicieron_su_eleccion()
            or await self.hay_tiempo_para_que_los_asesinos_voten()
        ):
            await contexto.send("Esperando a los asesinos...")
            await self.esperar_un_segundo_para_que_los_asesinos_voten()
        nick_de_la_victima = await self.nick_de_la_victima_elegida()
        partida.quitar_al_jugador_elegido_por_los_asesinos(nick_de_la_victima)
        return self

    async def hay_tiempo_para_que_los_asesinos_voten(self):
        async with self.votacion_en_proceso:
            return self.cantidad_de_asesinos_que_votan > 0

    async def asesinos_hicieron_su_eleccion(self):
        async with self.votacion_en_proceso:
            return self.cantidad_de_asesinos_que_votan == 0

    async def nick_de_la_victima_elegida(self):
        async with self.votacion_en_proceso:
            votaciones = self.urna_con_posibles_victimas.items()
            victima = max(votaciones, key=lambda x: x[1])
            return victima[0]

    async def esperar_un_segundo_para_que_los_asesinos_voten(self):
        await asyncio.sleep(1)
        self.cantidad_de_asesinos_que_votan -= 1

    async def un_asesino_esta_detras_de_alguien(
        self, nick_del_asesino: str, nick_de_la_victima: str, partida: Partida
    ):
        async with self.votacion_en_proceso:
            partida.verificar_si_el_asesino_esta_en_juego(nick_del_asesino)
            partida.verificar_si_la_victima_esta_en_juego(nick_de_la_victima)
            if nick_de_la_victima not in self.urna_con_posibles_victimas:
                self.urna_con_posibles_victimas[nick_de_la_victima] = 1
            else:
                self.urna_con_posibles_victimas[nick_de_la_victima] += 1

            self.cantidad_de_asesinos_que_votan -= 1
        return self
