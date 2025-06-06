from pydantic import BaseModel, ConfigDict
from typing import Optional

class PeriodoBase(BaseModel):
    periodo: str
    fecha_inicio: str
    fecha_fin: str

class PeriodoCrear(PeriodoBase):
    pass

class PeriodoEditar(BaseModel):
    periodo: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None

class PeriodoResponse(PeriodoBase):
    id_periodo: int

    model_config = ConfigDict(from_attributes=True)
