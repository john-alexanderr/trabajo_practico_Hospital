from models.paciente import PacienteActualizar, PacienteCrear
from routers.base import crear_crud_router

router = crear_crud_router(
    prefijo="/pacientes",
    tag="Pacientes",
    archivo="pacientes.json",
    modelo_crear=PacienteCrear,
    modelo_actualizar=PacienteActualizar,
    campo_unico="dni",
    nombre_campo="DNI",
)
