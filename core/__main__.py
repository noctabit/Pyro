import os
import sys
import time
import logging
from pyrogram import Client

def main():
    """Función principal del Userbot."""
    start_time = time.time()

    # ========================
    # CONFIGURACIÓN DEL LOGGER
    # ========================
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    logger = logging.getLogger("Userbot")

    # ========================
    # IMPORTAR CONFIGURACIONES
    # ========================
    try:
        from configs import Config  # Config carga las variables desde .env
    except ImportError:
        logger.error("No se pudo importar configs.py. Asegúrate de que existe y está configurado correctamente.")
        sys.exit(1)

    # ========================
    # VERIFICACIONES INICIALES
    # ========================
    logger.info("Realizando verificaciones iniciales...")

    # Verificar API_ID
    if not hasattr(Config, "API_ID") or not Config.API_ID:
        logger.critical("Falta la configuración 'API_ID' en el archivo .env. Revisa el archivo y vuelve a intentarlo.")
        sys.exit(1)

    # Verificar API_HASH
    if not hasattr(Config, "API_HASH") or not Config.API_HASH:
        logger.critical("Falta la configuración 'API_HASH' en el archivo .env. Revisa el archivo y vuelve a intentarlo.")
        sys.exit(1)

    # Verificar SESSION_STRING
    if not hasattr(Config, "SESSION_STRING") or not Config.SESSION_STRING:
        logger.critical(
            "Falta la configuración 'SESSION_STRING' en el archivo .env. Este campo es obligatorio para el Userbot."
        )
        sys.exit(1)

    # Verificar BOT_TOKEN
    if not hasattr(Config, "BOT_TOKEN") or not Config.BOT_TOKEN:
        logger.critical(
            "Falta la configuración 'BOT_TOKEN' en el archivo .env. Este campo es obligatorio para el bot asistente."
        )
        sys.exit(1)

    logger.info("Todas las configuraciones críticas están presentes.")

    # ========================
    # INICIALIZAR LOS CLIENTES
    # ========================
    logger.info("Inicializando el cliente de Pyrogram para el Userbot...")
    userbot_app = Client(
        "userbot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=Config.SESSION_STRING,
        plugins=dict(root="plugins/userbot"),
    )

    logger.info("Inicializando el cliente de Pyrogram para el bot asistente...")
    assistant_app = Client(
        "assistant_bot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="plugins/assistant"),
    )

    # ========================
    # LIMPIEZA Y PREPARACIÓN
    # ========================
    plugins_userbot_path = os.path.join(os.getcwd(), "plugins", "userbot")
    plugins_assistant_path = os.path.join(os.getcwd(), "plugins", "assistant")

    for path in [plugins_userbot_path, plugins_assistant_path]:
        if not os.path.exists(path):
            logger.warning(f"La carpeta '{path}' no existe. Creándola...")
            os.makedirs(path)
        else:
            logger.info(f"Plugins cargados desde: {path}")

    logger.info("Realizando limpieza de cachés... (placeholder)")

    # ========================
    # EJECUCIÓN FINAL
    # ========================
    logger.info(f"Tardó {round((time.time() - start_time) * 1000, 2)} ms en preparar el Userbot y el bot asistente.")
    try:
        userbot_app.start()
        logger.info("El Userbot está en funcionamiento.")

        assistant_app.start()
        logger.info("El bot asistente está en funcionamiento.")

        logger.info("Ambos clientes están activos. Esperando eventos...")
        userbot_app.idle()  # Mantiene los clientes activos hasta que se interrumpan
        assistant_app.stop()

    except Exception as e:
        logger.error(f"Error inesperado durante la ejecución: {e}")
        sys.exit(1)
    finally:
        userbot_app.stop()
        logger.info("El Userbot ha sido detenido.")

if __name__ == "__main__":
    main()
