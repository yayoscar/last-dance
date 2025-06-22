from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.alumno import AlumnoBase

class GrupoBase(BaseModel):
    tipo: str
    turno: str
    nombre: str

class GrupoCrear(GrupoBase):
    model_config = ConfigDict(from_attributes=True)

class GrupoResponse(GrupoBase):
    id_grupo: int
    model_config = ConfigDict(from_attributes=True)

class GrupoEditar(BaseModel):
    tipo: str | None = None
    turno: str | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)
