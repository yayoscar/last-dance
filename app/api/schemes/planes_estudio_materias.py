from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from app.api.schemes.carrera import CarreraResponse
from app.api.schemes.plan_estudio import PlanResponse
from app.api.schemes.materias import MateriaResponse


class MateriaAsignacion(BaseModel):
    id_materia: int
    semestre: int = Field(gt=0, lt=6)
    
    model_config = ConfigDict(from_attributes=True)

class PlanEstudioMateriaAgregar(BaseModel):
    materias: List[MateriaAsignacion]
    
    model_config = ConfigDict(from_attributes=True)

class MateriaPlanResponse(MateriaResponse):
    semestre: int
    
    model_config = ConfigDict(from_attributes=True)

class PlanEstudioConMateriasResponse(PlanResponse):
    id_plan_estudio: int
    nombre: str
    id_carrera: int
    carrera: Optional[CarreraResponse]  # Asegúrate de tener este esquema
    
    class Config:
        from_attributes = True
# Update forward references
PlanEstudioConMateriasResponse.model_rebuild()
MateriaPlanResponse.model_rebuild()