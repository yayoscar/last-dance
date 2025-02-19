from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.api.schemes.carrera import CarreraSchema


class AlumnoBase(BaseModel):
    nombre: str
    ape_paterno: str
    ape_materno: str
    num_control: str
    curp: str
    id_carrera: int
    turno: str
    generacion: int

class AlumnoCrear(BaseModel):
    pass

class AlumnoResponse(AlumnoBase):
    id_alumno: int
    carrera: Optional[CarreraSchema] = None 

    model_config = ConfigDict(from_attributes=True)
