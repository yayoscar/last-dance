from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.alumno import AlumnoBase

class CarreraSchema(BaseModel):
    id_carrera: Optional[int] = Field(None, exclude=True)
    nombre: str
    # alumnos: Optional[List[AlumnoBase]] = None
    model_config = ConfigDict(from_attributes=True)





    
    