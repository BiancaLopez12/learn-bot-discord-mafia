from bot import MafiaBotModerador
from discord.ext import commands
from juego import Mafia
from comandos.partida import extraer_cantidad_de_jugadores


juego = Mafia()
bot = MafiaBotModerador()


@bot.command()
async def estado(contexto: commands.Context):
    await contexto.send(f"Ok! {round(bot.latency * 1000)}ms")


@bot.command()
async def ayuda(contexto: commands.Context):
    comandos = ["estado", "ayuda", "crear", "unirse", "comenzar"]
    await contexto.send(f"Comandos disponibles: {', '.join(comandos)}")


@bot.command()
async def crear(contexto: commands.Context):
    try:
        cantidad_de_jugadores = extraer_cantidad_de_jugadores(contexto.message.content)
        juego.crear_partida(cantidad_de_jugadores)
        await contexto.send(
            f"Partida creada para {cantidad_de_jugadores} jugadores, para unirse usa !unirse"
        )
    except Exception as e:
        await contexto.send(f"{e}")


def main():
    bot.iniciar()


if __name__ == "__main__":
    main()
