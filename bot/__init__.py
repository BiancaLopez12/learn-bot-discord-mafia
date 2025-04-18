from dataclasses import dataclass
import logging
import discord
import os
from discord.ext import commands

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class MafiaBotModerador(commands.Bot):
    token = os.environ["DISCORD_TOKEN"]

    def __init__(self):
        permisos = discord.Intents.all()
        super().__init__(command_prefix="!", intents=permisos)

    async def on_ready(self):
        logging.info(f"Listo para jugar, mi nickname es {self.user}")

    def ejecutar(self):
        self.run(self.token)
