from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database.db import Base
from sqlalchemy import String

class Carrera(Base):
    __tablename__ = "carreras"

    id_carrera: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones
    alumnos: Mapped[list["Alumno"]] = relationship("Alumno", back_populates="carreras") #type: ignore
    planes_estudio: Mapped[list["PlanEstudio"]] = relationship("PlanEstudio", back_populates="carrera") #type: ignore
   