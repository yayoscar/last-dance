from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base

class Modulo(Base):
    __tablename__ = "modulos"
    
    id_modulo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    
    # Relación con Materia (corregido: referencia a la clase "Materia")
    materias = relationship("Materia", back_populates="modulo")