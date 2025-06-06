from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.alumno import AlumnoBase

from enum import Enum
class MateriaBase(BaseModel):
    nombre: str
    creditos: int
    tipo: TipoMateria  # Usa el Enum
    id_modulo: int | None = None  # Make it optional if needed
    
    class Config:
        from_attributes = True

class TipoMateria(str, Enum):
    MATERIA = "Materia"
    MODULO = "Módulo"  # Asegúrate que coincida con el frontend

class MateriaCrear(BaseModel):
    nombre: str
    creditos: int
    tipo: TipoMateria  # Usamos el Enum
    id_modulo: int | None = Field(
        None,
        description="Obligatorio solo para tipo Módulo"
    )

class MateriaResponse(MateriaBase):
    id_materia: int
    model_config = ConfigDict(from_attributes=True)
    
class MateriaEditar(MateriaBase):
    id_materia: int
