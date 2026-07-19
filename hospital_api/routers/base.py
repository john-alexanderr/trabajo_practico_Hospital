from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from auth.security import obtener_usuario_actual
from services.json_persistence import (
    actualizar_id,
    buscar_id,
    cargar_datos,
    eliminar_id,
    guardar_datos,
    siguiente_id,
)


def crear_crud_router(
    prefijo: str,
    tag: str,
    archivo: str,
    modelo_crear: type[BaseModel],
    modelo_actualizar: type[BaseModel],
    campo_unico: str | None = None,
    nombre_campo: str = "",
) -> APIRouter:
    router = APIRouter(prefix=prefijo, tags=[tag])

    @router.get("/")
    async def listar() -> list[dict]:
        return cargar_datos(archivo)

    @router.get("/{entidad_id}")
    async def buscar(entidad_id: int) -> dict:
        datos = cargar_datos(archivo)
        item = buscar_id(datos, entidad_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"{tag[:-1]} con ID {entidad_id} no encontrado.")
        return item

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def crear(
        datos_entrada: modelo_crear,
        usuario: Annotated[str, Depends(obtener_usuario_actual)],
    ) -> dict:
        datos = cargar_datos(archivo)
        if campo_unico:
            for item in datos:
                if item[campo_unico] == getattr(datos_entrada, campo_unico):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Ya existe un {tag[:-1].lower()} con {nombre_campo} {getattr(datos_entrada, campo_unico)}.",
                    )
        nuevo = {"id": siguiente_id(datos), **datos_entrada.model_dump()}
        datos.append(nuevo)
        guardar_datos(archivo, datos)
        return nuevo

    @router.put("/{entidad_id}")
    async def modificar(
        entidad_id: int,
        datos_entrada: modelo_actualizar,
        usuario: Annotated[str, Depends(obtener_usuario_actual)],
    ) -> dict:
        datos = cargar_datos(archivo)
        if buscar_id(datos, entidad_id) is None:
            raise HTTPException(status_code=404, detail=f"{tag[:-1]} con ID {entidad_id} no encontrado.")
        if campo_unico:
            for item in datos:
                if item[campo_unico] == getattr(datos_entrada, campo_unico) and item["id"] != entidad_id:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Ya existe otro {tag[:-1].lower()} con {nombre_campo} {getattr(datos_entrada, campo_unico)}.",
                    )
        datos = actualizar_id(datos, entidad_id, datos_entrada.model_dump())
        guardar_datos(archivo, datos)
        return {"id": entidad_id, **datos_entrada.model_dump()}

    @router.delete("/{entidad_id}")
    async def eliminar(
        entidad_id: int,
        usuario: Annotated[str, Depends(obtener_usuario_actual)],
    ) -> dict:
        datos = cargar_datos(archivo)
        if buscar_id(datos, entidad_id) is None:
            raise HTTPException(status_code=404, detail=f"{tag[:-1]} con ID {entidad_id} no encontrado.")
        datos = eliminar_id(datos, entidad_id)
        guardar_datos(archivo, datos)
        return {"mensaje": f"{tag[:-1]} con ID {entidad_id} eliminado correctamente."}

    return router
