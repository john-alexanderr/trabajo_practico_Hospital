from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from auth.security import obtener_usuario_actual
from models.internacion import InternacionActualizar, InternacionCrear
from services.json_persistence import (
    actualizar_id,
    buscar_id,
    cargar_datos,
    eliminar_id,
    guardar_datos,
    siguiente_id,
)

router = APIRouter(prefix="/internaciones", tags=["Internaciones"])


def _validar_referencias(paciente_id: int, medico_id: int) -> None:
    pacientes = cargar_datos("pacientes.json")
    if buscar_id(pacientes, paciente_id) is None:
        raise HTTPException(status_code=400, detail=f"Paciente ID {paciente_id} no existe.")
    medicos = cargar_datos("medicos.json")
    if buscar_id(medicos, medico_id) is None:
        raise HTTPException(status_code=400, detail=f"Médico ID {medico_id} no existe.")


@router.get("/")
async def listar() -> list[dict]:
    return cargar_datos("internaciones.json")


@router.get("/{internacion_id}")
async def buscar(internacion_id: int) -> dict:
    datos = cargar_datos("internaciones.json")
    item = buscar_id(datos, internacion_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Internación ID {internacion_id} no encontrada.")
    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(
    datos: InternacionCrear,
    usuario: Annotated[str, Depends(obtener_usuario_actual)],
) -> dict:
    _validar_referencias(datos.paciente_id, datos.medico_id)
    internaciones = cargar_datos("internaciones.json")
    nueva = {"id": siguiente_id(internaciones), **datos.model_dump()}
    internaciones.append(nueva)
    guardar_datos("internaciones.json", internaciones)
    return nueva


@router.put("/{internacion_id}")
async def modificar(
    internacion_id: int,
    datos: InternacionActualizar,
    usuario: Annotated[str, Depends(obtener_usuario_actual)],
) -> dict:
    internaciones = cargar_datos("internaciones.json")
    if buscar_id(internaciones, internacion_id) is None:
        raise HTTPException(status_code=404, detail=f"Internación ID {internacion_id} no encontrada.")
    _validar_referencias(datos.paciente_id, datos.medico_id)
    internaciones = actualizar_id(internaciones, internacion_id, datos.model_dump())
    guardar_datos("internaciones.json", internaciones)
    return {"id": internacion_id, **datos.model_dump()}


@router.delete("/{internacion_id}")
async def eliminar(
    internacion_id: int,
    usuario: Annotated[str, Depends(obtener_usuario_actual)],
) -> dict:
    internaciones = cargar_datos("internaciones.json")
    if buscar_id(internaciones, internacion_id) is None:
        raise HTTPException(status_code=404, detail=f"Internación ID {internacion_id} no encontrada.")
    internaciones = eliminar_id(internaciones, internacion_id)
    guardar_datos("internaciones.json", internaciones)
    return {"mensaje": f"Internación ID {internacion_id} eliminada correctamente."}
