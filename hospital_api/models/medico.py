from pydantic import BaseModel, Field, field_validator


class MedicoBase(BaseModel):
    matricula: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    especialidad: str = Field(min_length=1)
    telefono: str = Field(min_length=1)

    @field_validator("telefono")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El teléfono no puede estar vacío.")
        return v


class MedicoCrear(MedicoBase):
    pass


class MedicoActualizar(MedicoBase):
    pass


class Medico(MedicoBase):
    id: int
