from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import String
from app.database.models.plan_estudio_materia import plan_estudio_materias


class PlanEstudio(Base):
    __tablename__ = "planes_estudio"

    id_plan_estudio: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones
    carreras: Mapped[list["Carrera"]] = relationship("Carrera", back_populates="plan_estudio") #type: ignore
    materias: Mapped[list["Materia"]] = relationship(secondary=plan_estudio_materias, back_populates="planes_estudio") #type: ignore