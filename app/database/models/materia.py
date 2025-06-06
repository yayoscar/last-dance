from sqlalchemy import Column, Integer, String, ForeignKey, insert
from sqlalchemy.orm import relationship
from app.database.db import Base # Importa la tabla
# En plan_estudio.py


class Materia(Base):
    __tablename__ = "materias" # Usa __table__ para acceso directo
    id_materia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    creditos = Column(Integer)
    tipo = Column(String)
    id_modulo = Column(Integer, ForeignKey("modulos.id_modulo"), nullable=True)
    
    # Relaciones
    modulo = relationship("Modulo", back_populates="materias")
    planes_estudio = relationship(
        "PlanEstudio",
        secondary="plan_estudio_materia",
        back_populates="materias",
        overlaps="planes_estudio_asociados"
    )
    
    planes_estudio_asociados = relationship(
        "PlanEstudioMateria",
        back_populates="materia",
        overlaps="planes_estudio"
    )