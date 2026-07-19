from models.medico import MedicoActualizar, MedicoCrear
from routers.base import crear_crud_router

router = crear_crud_router(
    prefijo="/medicos",
    tag="Médicos",
    archivo="medicos.json",
    modelo_crear=MedicoCrear,
    modelo_actualizar=MedicoActualizar,
    campo_unico="matricula",
    nombre_campo="matrícula",
)
