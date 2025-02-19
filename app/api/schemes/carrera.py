from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.alumno import AlumnoBase

class CarreraBase(BaseModel):
    nombre: str

class CarreraCrear(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id_carrera: int

    model_config = ConfigDict(from_attributes=True)
    
class CarreraEditar(CarreraBase):
    id_carrera: int



    
    