# Mafia With Discord

Mafia With Discord es una reversión del juego de mesa "mafia" que utiliza un bot de Discord para moderar una sesión del juego. El bot está desarrollado con la librería `discord.py`, es decir, está escrito principalmente en Python.

## Requisitos

- Python 3.8 o superior
- pipenv

## Instalación

Para instalar las dependencias tanto de desarrollo como de ejecución, se debe correr el siguiente comando:

```bash
pipenv install -d
```

## Configuración

Antes de ejecutar el bot, debe configurarse el entorno de desarrollo. Para ello, debe crearse un archivo `.env` en la raíz del proyecto conteniendo la variable de entorno que se muestra en el archivo de ejemplo `.env.example`. La misma variable debe estar configurada en un entorno de producción.

## Uso

### Entorno de Producción

Para ejecutar el bot en un entorno de producción, se debe correr el comando:

```bash
pipenv run start
```

### Entorno de Desarrollo

Para ejecutar el bot en un entorno de desarrollo, se debe correr el comando:

```bash
pipenv run dev
```

### Tests

Para correr los tests básicos, se debe ejecutar el comando:

```bash
pipenv run tests
```

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, sigue las siguientes pautas para contribuir al proyecto:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit de ellos (`git commit -m 'Agregar nueva funcionalidad'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request en este repositorio.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Créditos

Desarrollado por [joackob](https://github.com/joackob).
