from dataclasses import dataclass
from discord import User, Member


@dataclass
class Rol:
    nombre: str = "Rol Generico"

    def __str__(self) -> str:
        return f"{self.nombre}"

    def soy_un_mafioso(self) -> bool:
        return False

    async def quien_sera_tu_victima(self, jugador: Member | User):
        return self


@dataclass
class Detective(Rol):
    def __init__(self):
        super().__init__(nombre="Detective")


@dataclass
class Ciudadano(Rol):
    def __init__(self):
        super().__init__(nombre="Ciudadano")


@dataclass
class Doctor(Rol):
    def __init__(self):
        super().__init__(nombre="Doctor")


@dataclass
class Mafioso(Rol):
    def __init__(self):
        super().__init__(nombre="Mafioso")

    def soy_un_mafioso(self) -> bool:
        return True

    async def quien_sera_tu_victima(self, jugador: Member | User):
        await jugador.send(
            "¿A quién vas a matar? Responde con el nombre del jugador o su ID."
        )
        return self
