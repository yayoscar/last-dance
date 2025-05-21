from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.controllers import carrera, periodo, plan_estudio,materias
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
        },
        {
            "name": "Planes_estudio",
            "description": "Operaciones relacionadas con los planes de estudio ."
        },
        {
            "name": "Periodos",
            "description": "Operaciones relacionadas con los periodos ."
        }
        
    ])

origins = [
    "http://localhost:3000",  # ejemplo: frontend en React
    "http://127.0.0.1:3000",
    # Puedes agregar más orígenes aquí
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para permitir todos los orígenes (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],     # Permite todos los métodos: GET, POST, etc.
    allow_headers=["*"],     # Permite todos los headers
)

v1_router = APIRouter(prefix="/api/v1")

# Agregar Rutas  a la principal  
v1_router.include_router(carrera.router, prefix="/carreras", tags=["Carreras"])
v1_router.include_router(alumno.router, prefix="/alumnos", tags=["Alumnos"])
v1_router.include_router(plan_estudio.router, prefix="/planes_estudio", tags=["Planes_estudio"])
v1_router.include_router(materias.router, prefix="/materias", tags=["Materias"])
v1_router.include_router(periodo.router, prefix="/periodos", tags=["Periodos"])

app.include_router(v1_router)
