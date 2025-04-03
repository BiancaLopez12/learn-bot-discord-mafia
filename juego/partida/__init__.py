from dataclasses import dataclass
from juego.jugador import Jugador, JugadorNPC, JugadorReal
import asyncio


class LaPartidaYaEstaCompletaYNoAceptaMasJugadores(Exception):
    def __str__(self):
        return "La partida ya está completa y no acepta más jugadores."


@dataclass
class Partida:
    def __init__(self, cantidad_de_jugadores: int = 0):
        self.cantidad_de_jugadores = cantidad_de_jugadores
        self.jugadores: list[Jugador] = []

    def agregar_jugador_si_es_posible(self, jugador):
        if len(self.jugadores) in range(0, self.cantidad_de_jugadores):
            self.jugadores.append(JugadorReal(jugador))
            return self
        raise LaPartidaYaEstaCompletaYNoAceptaMasJugadores()

    def completar_partida_si_es_necesario(self):
        cantidad_de_jugadores_faltantes = self.cantidad_de_jugadores - len(
            self.jugadores
        )
        for _ in range(cantidad_de_jugadores_faltantes):
            self.jugadores.append(JugadorNPC())

        return self

    def asignar_roles(self):
        for jugador in self.jugadores:
            jugador.seleccionar_rol()
        return self

    def proximo_aviso_a_realizar(self):
        for jugador in self.jugadores:
            yield jugador.comunicar_rol_al_usuario()

    async def comunicar_roles_por_mp(self):
        avisos = [aviso for aviso in self.proximo_aviso_a_realizar()]
        await asyncio.gather(*avisos)
        return self
