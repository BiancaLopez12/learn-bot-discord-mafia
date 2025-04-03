from bot import MafiaBotModerador
from discord.ext import commands
from juego import Mafia
from utils.crear_partida import extraer_cantidad_de_jugadores


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
        await contexto.send(f"Partida creada para {cantidad_de_jugadores} jugadores.")
        await contexto.send("Para unirse deben usar el comando !unirse")
    except Exception as e:
        await contexto.send(f"{e}")


@bot.command()
async def unirse(contexto: commands.Context):
    try:
        juego.agregar_jugador(contexto.author)
        await contexto.send(f"{contexto.author.name} se unió a la partida.")
    except Exception as e:
        await contexto.send(f"{e}")


@bot.command()
async def comenzar(contexto: commands.Context):
    try:
        await juego.comenzar()
        await contexto.send("La partida ha comenzado!")
        await contexto.send("Pronto todos recibiran sus roles. Esperen un momento.")
    except Exception as e:
        await contexto.send(f"{e}")


def main():
    bot.iniciar()


if __name__ == "__main__":
    main()
