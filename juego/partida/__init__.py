from dataclasses import dataclass

from juego.jugador import Jugador, JugadorNPC, JugadorReal


class LaPartidaYaEstaCompleta(Exception):
    def __str__(self):
        return "Ya hay suficientes jugadores en la partida."


@dataclass
class Partida:
    def __init__(self, cantidad_de_jugadores: int = 0):
        self.cantidad_de_jugadores = cantidad_de_jugadores
        self.jugadores: list[Jugador] = []

    def agregar_jugador_si_es_posible(self, jugador):
        if len(self.jugadores) == self.cantidad_de_jugadores:
            raise LaPartidaYaEstaCompleta()
        self.jugadores.append(JugadorReal(jugador))
        if len(self.jugadores) == self.cantidad_de_jugadores:
            raise LaPartidaYaEstaCompleta()
        return self

    def completar_partida_si_es_necesario(self):
        if len(self.jugadores) == self.cantidad_de_jugadores:
            return self
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

    async def comunicar_roles_por_mp(self):
        for jugador in self.jugadores:
            await jugador.comunicar_rol_al_usuario()
        pass
