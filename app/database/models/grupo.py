from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import String, ForeignKey

class Grupo(Base):
    __tablename__ = "grupos"

    id_grupo: Mapped[int] = mapped_column(primary_key=True)
    id_periodo: Mapped[int] = mapped_column(ForeignKey("periodos.id_periodo"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(255), nullable=False)
    turno: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones 
    periodo: Mapped["Periodo"] = relationship("Periodo", back_populates="grupos") #type: ignore
    grupo_alumnos: Mapped[list["GrupoAlumno"]] = relationship("GrupoAlumno", back_populates="grupo") #type: ignore