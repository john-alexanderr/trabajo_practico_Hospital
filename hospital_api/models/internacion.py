from pydantic import BaseModel, Field, field_validator

ESTADOS_VALIDOS = ["activa", "alta", "derivada", "fallecido"]


class InternacionBase(BaseModel):
    paciente_id: int
    medico_id: int
    fecha_ingreso: str = Field(min_length=1)
    diagnostico: str = Field(min_length=1)
    habitacion: int = Field(gt=0)
    estado: str = Field(min_length=1)

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Permitidos: {', '.join(ESTADOS_VALIDOS)}")
        return v


class InternacionCrear(InternacionBase):
    pass


class InternacionActualizar(InternacionBase):
    pass


class Internacion(InternacionBase):
    id: int
