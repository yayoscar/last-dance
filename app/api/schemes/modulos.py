from pydantic import BaseModel

class ModuloBase(BaseModel):
    nombre: str

class ModuloCreate(ModuloBase):
    pass

class Modulo(ModuloBase):
    id_modulo: int
    
    class Config:
        from_attributes = True  # Esto permite la conversión desde ORM