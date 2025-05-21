from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# from app.api.schemes.periodo import PeriodoBase

class PeriodoBase(BaseModel):
    nombre: str

class PeriodoCrear(PeriodoBase):
    pass

class PeriodoResponse(PeriodoBase):
    id_periodo: int

    model_config = ConfigDict(from_attributes=True)
    
class PeriodoEditar(PeriodoBase):
    id_periodo: int



    
    