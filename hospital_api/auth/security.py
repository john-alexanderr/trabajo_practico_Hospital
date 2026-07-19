import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

CLAVE_SECRETA = os.environ.get("JWT_SECRET", "cambiar_en_produccion")
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = int(os.environ.get("JWT_EXPIRACION_MINUTOS", "60"))

USUARIO_ADMIN = os.environ.get("ADMIN_USER", "admin")
CONTRASENA_ADMIN = os.environ.get("ADMIN_PASS", "hospital2024")

oauth2 = OAuth2PasswordBearer(tokenUrl="login", auto_error=True)


class Token(BaseModel):
    access_token: str
    token_type: str


def verificar_credenciales(usuario: str, contrasena: str) -> bool:
    return usuario == USUARIO_ADMIN and contrasena == CONTRASENA_ADMIN


def crear_token(datos: dict, expiracion: timedelta | None = None) -> str:
    payload = datos.copy()
    exp = datetime.now(timezone.utc) + (expiracion or timedelta(minutes=MINUTOS_EXPIRACION))
    payload.update({"exp": exp})
    return jwt.encode(payload, CLAVE_SECRETA, algorithm=ALGORITMO)


async def obtener_usuario_actual(token: Annotated[str, Depends(oauth2)]) -> str:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        usuario = payload.get("sub")
        if usuario is None:
            raise exc
        return usuario
    except JWTError:
        raise exc


async def login(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    if not verificar_credenciales(form.username, form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_token({"sub": form.username})
    return Token(access_token=token, token_type="bearer")
