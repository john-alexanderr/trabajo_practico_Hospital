<div align="center">

# 🏥 Sistema de Gestión Hospitalaria

**Trabajo Práctico - Programación Avanzada**

API RESTful + Cliente de Consola para la gestión de pacientes, médicos e internaciones.

---

</div>

## 📋 Descripción

Sistema cliente-servidor desarrollado en Python que permite administrar un hospital de forma integral. La **API REST** provee los endpoints CRUD protegidos con autenticación JWT, y el **cliente de consola** ofrece una interfaz interactiva para consumirlos.

## 🧱 Stack Tecnológico

| Componente | Tecnología |
|---|---|
| API | FastAPI + Uvicorn |
| Cliente | Python + Requests |
| Autenticación | JWT (python-jose) |
| Validación | Pydantic v2 |
| Persistencia | Archivos JSON |

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/john-alexanderr/trabajo_practico_Hospital.git
cd trabajo_practico_Hospital
```

### 2. Instalar dependencias

```bash
cd hospital_api
pip install -r requirements.txt
```

### 3. Iniciar la API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La documentación interactiva (Swagger) estará disponible en:
➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Iniciar el cliente

En una **nueva terminal**:

```bash
cd hospital_client
python main.py
```

## 🔐 Credenciales

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `hospital2024` |

> Las credenciales pueden configurarse mediante variables de entorno (`ADMIN_USER`, `ADMIN_PASS`) o un archivo `.env`.

## 📁 Estructura del Proyecto

```
hospital-api-client-main/
├── hospital_api/          # API REST (FastAPI)
│   ├── auth/              # Autenticación JWT
│   ├── data/              # Datos persistidos (JSON)
│   ├── models/            # Modelos Pydantic
│   ├── routers/           # Endpoints CRUD
│   ├── services/          # Persistencia y lógica
│   ├── requirements.txt
│   └── main.py
├── hospital_client/       # Cliente de consola
│   ├── client/            # Lógica del cliente
│   ├── main.py
│   └── logs.txt
├── seed_inicio/           # Datos de prueba iniciales
├── Integrantes.txt
└── README.md
```

## 📡 Endpoints de la API

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/` | ❌ | Estado de la API |
| `POST` | `/login` | ❌ | Iniciar sesión |
| `GET` | `/pacientes` | ❌ | Listar pacientes |
| `POST` | `/pacientes` | ✅ | Crear paciente |
| `PUT` | `/pacientes/{id}` | ✅ | Modificar paciente |
| `DELETE` | `/pacientes/{id}` | ✅ | Eliminar paciente |
| `GET` | `/medicos` | ❌ | Listar médicos |
| `POST` | `/medicos` | ✅ | Crear médico |
| `PUT` | `/medicos/{id}` | ✅ | Modificar médico |
| `DELETE` | `/medicos/{id}` | ✅ | Eliminar médico |
| `GET` | `/internaciones` | ❌ | Listar internaciones |
| `POST` | `/internaciones` | ✅ | Crear internación |
| `PUT` | `/internaciones/{id}` | ✅ | Modificar internación |
| `DELETE` | `/internaciones/{id}` | ✅ | Eliminar internación |

---

<div align="center">

**Desarrollado por Juan Rastellini** · Grupo 20

</div>
