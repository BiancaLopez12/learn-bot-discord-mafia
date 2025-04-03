from dataclasses import dataclass


@dataclass
class Rol:
    nombre: str = "Rol Generico"

    def __str__(self) -> str:
        return f"{self.nombre}"


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
class Asesino(Rol):
    def __init__(self):
        super().__init__(nombre="Asesino")
