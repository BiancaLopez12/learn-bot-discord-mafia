from dataclasses import dataclass
import logging
import discord
import os


@dataclass
class MafiaBotModerador(discord.Client):
    token = os.environ["DISCORD_TOKEN"]

    def __init__(self):
        intentosParaReconexion = discord.Intents.default()
        intentosParaReconexion.message_content = True
        super().__init__(intents=intentosParaReconexion)

    async def on_ready(self):
        logging.info(f"Listo para jugar, mi nickname es {self.user}")

    def iniciar(self):
        self.run(self.token)
