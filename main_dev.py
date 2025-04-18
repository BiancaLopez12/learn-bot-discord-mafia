import time
import logging
import uuid
import subprocess
import sys
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class BotEnDesarrollo(subprocess.Popen):
    comando = [sys.executable, "main.py"]
    id = int(uuid.uuid4())

    def __init__(self):
        super().__init__(self.comando)

    def __hash__(self):
        return self.id

    def reiniciar(self):
        logging.info("Reiniciando el bot")
        self.terminate()
        self.wait()
        super().__init__(self.comando)

    def detener(self):
        logging.info("Deteniendo el bot")
        self.terminate()
        self.wait()


@dataclass
class EntornoDeDesarrollo(FileSystemEventHandler):
    bot = BotEnDesarrollo()
    observador = Observer()
    id = int(uuid.uuid4())

    def __hash__(self):
        return self.id

    # evento a gestionar
    def on_modified(self, event):
        self.reiniciar_si_hubo_cambios_en_el_proyecto(event)

    def reiniciar_si_hubo_cambios_en_el_proyecto(self, evento):
        if self.hubo_cambios_en_el_proyecto(evento):
            self.bot.reiniciar()

    def hubo_cambios_en_el_proyecto(self, evento):
        return str(evento.src_path).endswith(".py")

    def comenzar_a_observar_cambios(self):
        logging.info("Iniciando el observador")
        self.observador.schedule(event_handler=self, path=".", recursive=True)
        self.observador.start()
        while True:
            time.sleep(1)

    def dejar_de_observar_cambios(self):
        logging.info("Deteniendo el observador")
        self.observador.stop()
        self.observador.join()

    def observar_cambios_en_el_proyecto(self):
        try:
            self.comenzar_a_observar_cambios()
        finally:
            self.dejar_de_observar_cambios()
            self.bot.detener()


def main():
    entorno = EntornoDeDesarrollo()
    entorno.observar_cambios_en_el_proyecto()


if __name__ == "__main__":
    main()
