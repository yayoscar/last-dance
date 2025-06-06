from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from app.api.schemes.carrera import CarreraBase

class PlanCrear(BaseModel):
    nombre: str
    id_carrera: int

class PlanEditar(BaseModel):
    nombre: str
    id_carrera: int

class PlanResponse(BaseModel):
    id_plan_estudio: int
    nombre: str
    id_carrera: int
    carrera: Optional[CarreraBase] = None  # Nota: sin comillas ahora

    class Config:
        from_attributes = True