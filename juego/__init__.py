from dataclasses import dataclass


@dataclass
class Mafia:
    cantiddad_de_jugadores: int = 0

    def crear_partida(self, cantidad_de_jugadores: int):
        self.cantiddad_de_jugadores = cantidad_de_jugadores
        return self
