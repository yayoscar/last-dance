from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Esquema base para Periodo (para evitar importación circular)
class PeriodoBase(BaseModel):
    id_periodo: int
    nombre: str

class GrupoBase(BaseModel):
    nombre: str
    id_periodo: int
    turno: str
    tipo: str

class GrupoCrear(GrupoBase):
    pass

class GrupoResponse(GrupoBase):
    id_grupo: int  
    periodo: Optional[PeriodoBase] = None

    model_config = ConfigDict(from_attributes=True)
    
class GrupoEditar(BaseModel):
    nombre: str
    id_periodo: int
    turno: str
    tipo: str
    

class AlumnoAsignacion(BaseModel):
    id_alumno: int
    semestre: int = Field(gt=0, lt=13, description="Semestre entre 1 y 12")

class GrupoAlumnoAgregar(BaseModel):
    alumnos: List[AlumnoAsignacion]

class AlumnoGrupoResponse(BaseModel):
    id_alumno: int
    nombre: str
    ape_paterno: str
    ape_materno: str
    num_control: str
    curp: str
    turno: str
    generacion: str
    semestre: int  


class GrupoConAlumnosResponse(BaseModel):
    id_grupo: int
    nombre: str
    turno: str
    tipo: str
    id_periodo: int
    periodo: Optional[PeriodoBase] = None
    alumnos: List[AlumnoGrupoResponse]

    model_config = ConfigDict(from_attributes=True)