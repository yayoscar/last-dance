from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import ForeignKey, Integer


class PlanEstudioMateria(Base):
    __tablename__ = "plan_estudio_materias"

    id_plan_estudio_materia: Mapped[int] = mapped_column(primary_key=True)
    id_materia: Mapped[int] = mapped_column(ForeignKey("materias.id_materia"), nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)
    id_carrera: Mapped[int] = mapped_column(ForeignKey("carreras.id_carrera"), nullable=False)
    id_plan_estudio: Mapped[int] = mapped_column(ForeignKey("planes_estudio.id_plan_estudio"), nullable=False)

    # Relaciones

    plan_estudio: Mapped["PlanEstudio"] = relationship("PlanEstudio", back_populates="plan_estudio_materias") #type: ignore
    materia: Mapped["Materia"] = relationship("Materia", back_populates="plan_estudio_materias") #type: ignore