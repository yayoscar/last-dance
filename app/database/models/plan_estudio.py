from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import ForeignKey, String
from app.database.models.plan_estudio_materia import plan_estudio_materias


class PlanEstudio(Base):
    __tablename__ = "planes_estudio"

    id_plan_estudio: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones
    id_carrera: Mapped[int] = mapped_column(ForeignKey("carreras.id_carrera"), nullable=False)
    carrera: Mapped["Carrera"] = relationship("Carrera", back_populates="planes_estudio")

    materias: Mapped[list["Materia"]] = relationship( #type: ignore
        secondary=plan_estudio_materias, back_populates="planes_estudio" 
    )

    alumnos: Mapped[list["Alumno"]] = relationship("Alumno", back_populates="plan_estudio")