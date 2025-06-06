from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import ForeignKey, String
class PlanEstudio(Base):
    __tablename__ = "planes_estudio"

    id_plan_estudio: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones
    id_carrera: Mapped[int] = mapped_column(ForeignKey("carreras.id_carrera"), nullable=False)
    carrera: Mapped["Carrera"] = relationship("Carrera", back_populates="planes_estudio") #type: ignore
    materias = relationship(
        "Materia",
        secondary="plan_estudio_materia",
        back_populates="planes_estudio",
        overlaps="materias_asociadas"
    )
    
    materias_asociadas = relationship(
        "PlanEstudioMateria",
        back_populates="plan_estudio",
        overlaps="materias"
    )