from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.alumno import AlumnoBase

class MateriaBase(BaseModel):
    nombre: str

class MateriaCrear(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id_materia: int

    model_config = ConfigDict(from_attributes=True)
    
class MateriaEditar(MateriaBase):
    id_materia: int
