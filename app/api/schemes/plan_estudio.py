from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.alumno import AlumnoBase

class PlanBase(BaseModel):
    nombre: str

class PlanCrear(PlanBase):
    pass

class PlanResponse(PlanBase):
    id_plan: int

    model_config = ConfigDict(from_attributes=True)
    
class PlanEditar(PlanBase):
    id_plan: int

class MateriaAsignacion(BaseModel):
    id_materia: int
    semestre: int = Field(gt=0, lt=13, description="Semestre entre 1 y 12")

class PlanEstudioMateriaAgregar(BaseModel):
    materias: List[MateriaAsignacion]

class MateriaPlanResponse(BaseModel):
    id_materia: int
    nombre: str
    creditos: int
    tipo: str
    id_modulo: int
    semestre: int  # Viene de la tabla intermedia

class PlanEstudioConMateriasResponse(BaseModel):
    id_plan_estudio: int
    nombre: str
    materias: List[MateriaPlanResponse]

    model_config = ConfigDict(from_attributes=True)