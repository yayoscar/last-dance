from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import String,Integer
from app.database.models.plan_estudio_materia import plan_estudio_materias

class Materia(Base):
    __tablename__ = "materias"

    id_materia: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(255), nullable=False)
    id_modulo: Mapped[int] = mapped_column(nullable=False)

    # Relaciones
    planes_estudio: Mapped[list["PlanEstudio"]] = relationship(secondary=plan_estudio_materias, back_populates="materias") #type: ignore