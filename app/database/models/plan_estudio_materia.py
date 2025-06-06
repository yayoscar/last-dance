from sqlalchemy import Column, Integer, ForeignKey
from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class PlanEstudioMateria(Base):
    __tablename__ = "plan_estudio_materia"
    id_plan_estudio = Column(Integer, ForeignKey("planes_estudio.id_plan_estudio"), primary_key=True)
    id_materia = Column(Integer, ForeignKey("materias.id_materia"), primary_key=True)
    semestre = Column(Integer)

    # Relaciones opcionales
    plan_estudio = relationship(
        "PlanEstudio",
        back_populates="materias_asociadas",
        overlaps="materias"
    )
    
    materia = relationship(
        "Materia",
        back_populates="planes_estudio_asociados",
        overlaps="planes_estudio"
    )