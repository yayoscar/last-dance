from fastapi import APIRouter, FastAPI
from app.api.controllers import carrera
from app.api.controllers import alumno

app = FastAPI(title="Sistema de Gestión de Carreras",
    description="API para reporte de calificaciones [last-dance].",
    version="1.0.0",
    contact={
        "name": "Soporte Técnico",
        "email": "soporte@example.com",
        "url": "https://example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Carreras",
            "description": "Operaciones relacionadas con las carreras universitarias."
        },
        {
            "name": "Alumnos",
            "description": "Operaciones relacionadas con los alumnos."
        }
    ])


v1_router = APIRouter(prefix="/api/v1")

# Agregar Rutas  a la principal  
v1_router.include_router(carrera.router, prefix="/carreras", tags=["Carreras"])
v1_router.include_router(alumno.router, prefix="/alumnos", tags=["Alumnos"])


app.include_router(v1_router)
