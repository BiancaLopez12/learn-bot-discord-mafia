from bot import MafiaBotModerador
from discord.ext import commands
from juego import Mafia
from utils.crear_partida import extraer_cantidad_de_jugadores
from utils.matar_ciudadano import extraer_nick_de_la_victima


juego = Mafia()
bot = MafiaBotModerador()


@bot.command()
async def estado(contexto: commands.Context):
    await contexto.send(f"Ok! {round(bot.latency * 1000)}ms")


@bot.command()
async def ayuda(contexto: commands.Context):
    comandos = ["estado", "ayuda", "jugar", "unirse", "comenzar"]
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
async def jugar(contexto: commands.Context):
    try:
        await contexto.send("La partida ha comenzado!")
        await contexto.send("Pronto todos recibiran sus roles. Esperen un momento.")
        await juego.asignar_roles_a_los_jugadores()
        await juego.informar_la_configuracion_de_la_partida(contexto)
        await juego.jugar_mientras_no_exista_un_equipo_ganador(contexto)
        await juego.informar_el_equipo_ganador(contexto)
    except Exception as e:
        await contexto.send(f"{e}")


@bot.command()
async def matar(contexto: commands.Context):
    try:
        await juego.un_mafioso_esta_detras_de_alguien(
            nick_del_mafioso=contexto.author.name,
            nick_de_la_victima=extraer_nick_de_la_victima(contexto.message.content),
        )
        await contexto.send("Un mafioso esta detras de alguien")
    except Exception as e:
        await contexto.author.send(f"{e}")


def main():
    bot.ejecutar()


if __name__ == "__main__":
    main()
