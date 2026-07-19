import json
import os
import threading
from typing import Any

DIRECTORIO_DATOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_lock = threading.Lock()


def _ruta(nombre_archivo: str) -> str:
    return os.path.join(DIRECTORIO_DATOS, nombre_archivo)


def cargar_datos(nombre_archivo: str) -> list[dict[str, Any]]:
    with _lock:
        try:
            with open(_ruta(nombre_archivo), "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos if isinstance(datos, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []


def guardar_datos(nombre_archivo: str, datos: list[dict[str, Any]]) -> None:
    with _lock:
        os.makedirs(os.path.dirname(_ruta(nombre_archivo)), exist_ok=True)
        with open(_ruta(nombre_archivo), "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)


def siguiente_id(datos: list[dict[str, Any]]) -> int:
    return max((item["id"] for item in datos), default=0) + 1


def buscar_id(datos: list[dict[str, Any]], id_buscado: int) -> dict[str, Any] | None:
    for item in datos:
        if item["id"] == id_buscado:
            return item
    return None


def eliminar_id(datos: list[dict[str, Any]], id_eliminar: int) -> list[dict[str, Any]]:
    return [item for item in datos if item["id"] != id_eliminar]


def actualizar_id(
    datos: list[dict[str, Any]],
    id_actualizar: int,
    nuevos_datos: dict[str, Any],
) -> list[dict[str, Any]]:
    resultado = []
    for item in datos:
        if item["id"] == id_actualizar:
            resultado.append({"id": id_actualizar, **nuevos_datos})
        else:
            resultado.append(item)
    return resultado
