#Crea un esquema pyndatic para el modelo Alumno
from pydantic import BaseModel
from typing import Optional

class AlumnoBase(BaseModel):
    nombre: str
    ape_paterno: str
    ape_materno: str
    num_control: str
    curp: str
    turno: str
    local: str
    generacion: str

class AlumnoCreate(AlumnoBase):
    pass    

class AlumnaEdit(AlumnoBase):
    id_alumno: int

