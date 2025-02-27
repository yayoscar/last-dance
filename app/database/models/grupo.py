from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import String, ForeignKey
from app.database.models.grupo_alumno import grupo_alumnos

class Grupo(Base):
    __tablename__ = "grupos"

    id_grupo: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255), nullable=False)
    turno: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones 
    id_periodo: Mapped[int] = mapped_column(ForeignKey("periodos.id_periodo"), nullable=False)
    periodo: Mapped["Periodo"] = relationship("Periodo", back_populates="grupos") #type: ignore
    
    alumnos: Mapped[list["Alumno"]] = relationship(secondary=grupo_alumnos, back_populates="grupos") #type: ignore