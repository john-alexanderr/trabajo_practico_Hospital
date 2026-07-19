from pydantic import BaseModel, Field, field_validator


class PacienteBase(BaseModel):
    dni: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    edad: int = Field(gt=0)
    telefono: str = Field(min_length=1)
    obra_social: str = Field(min_length=1)

    @field_validator("dni")
    @classmethod
    def validar_dni(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit():
            raise ValueError("El DNI debe contener solo números.")
        return v

    @field_validator("telefono", "obra_social")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Este campo no puede estar vacío.")
        return v


class PacienteCrear(PacienteBase):
    pass


class PacienteActualizar(PacienteBase):
    pass


class Paciente(PacienteBase):
    id: int
