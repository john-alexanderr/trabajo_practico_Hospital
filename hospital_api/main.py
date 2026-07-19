from os.path import dirname, join

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(join(dirname(__file__), ".env"))

from auth.security import login
from routers import internaciones, medicos, pacientes

app = FastAPI(
    title="Sistema de Gestión Hospitalaria",
    version="0.2.0",
)

app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(internaciones.router)
app.post("/login", tags=["Autenticación"])(login)


@app.get("/")
async def raiz() -> dict:
    return {"mensaje": "Sistema de Gestión Hospitalaria - API activa.", "documentacion": "/docs"}
