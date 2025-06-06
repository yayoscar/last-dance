from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.controllers import carrera, plan_estudio, materias, alumno, periodo  # <-- Importa periodos aquí

app = FastAPI(
    title="Sistema de Gestión de Carreras",
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
        },
        {
            "name": "Planes_estudio",
            "description": "Operaciones relacionadas con los planes de estudio."
        },
        {
            "name": "Periodos",          # <-- Agrega la sección para periodos
            "description": "Operaciones relacionadas con los periodos escolares."
        },
        {
            "name": "Materias",
            "description": "Operaciones relacionadas con las materias."
        }
    ]
)

origins = [
    "*",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

v1_router = APIRouter(prefix="/api/v1")

# Agregar Rutas a la principal  
v1_router.include_router(carrera.router, prefix="/carreras", tags=["Carreras"])
v1_router.include_router(alumno.router, prefix="/alumnos", tags=["Alumnos"])
v1_router.include_router(plan_estudio.router, prefix="/planes_estudio", tags=["Planes_estudio"])
v1_router.include_router(materias.router, prefix="/materias", tags=["Materias"])
v1_router.include_router(periodo.router, prefix="/periodos", tags=["Periodos"])  # <-- Aquí agregas periodos

app.include_router(v1_router)
