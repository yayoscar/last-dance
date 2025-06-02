from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Esquema base para Carrera (para evitar importación circular)
class CarreraBase(BaseModel):
    id_carrera: int
    nombre: str

class PlanBase(BaseModel):
    nombre: str
    id_carrera: int

class PlanCrear(PlanBase):
    pass

class PlanResponse(PlanBase):
    id_plan_estudio: int  # Corregido: era id_plan
    carrera: Optional[CarreraBase] = None

    model_config = ConfigDict(from_attributes=True)
    
class PlanEditar(BaseModel):
    nombre: str
    id_carrera: int

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
    id_carrera: int
    carrera: Optional[CarreraBase] = None
    materias: List[MateriaPlanResponse]

    model_config = ConfigDict(from_attributes=True)