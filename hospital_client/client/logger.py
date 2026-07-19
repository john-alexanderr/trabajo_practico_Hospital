import os
from datetime import datetime

RUTA_LOG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs.txt")


def registrar_log(usuario: str, operacion: str) -> None:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(RUTA_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{fecha}] Usuario: {usuario} | Operación: {operacion}\n")
    except OSError:
        pass
