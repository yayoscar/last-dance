from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import String,Integer

class Materia(Base):
    __tablename__ = "materias"

    id_materia: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(255), nullable=False)
    id_modulo: Mapped[int] = mapped_column(nullable=False)

    # Relaciones
    plan_estudio_materias: Mapped[list["PlanEstudioMateria"]] = relationship("PlanEstudioMateria", back_populates="materia") #type: ignore