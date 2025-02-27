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
