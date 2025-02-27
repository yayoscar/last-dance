from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import BigInteger, Integer, String, ForeignKey
from app.database.models.grupo_alumno import grupo_alumnos


class Alumno(Base):
    __tablename__ = "alumnos"

    id_alumno: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ape_paterno: Mapped[str] = mapped_column(String(255), nullable=False)
    ape_materno: Mapped[str] = mapped_column(String(255), nullable=False)
    num_control: Mapped[str] = mapped_column(String, nullable=False)
    curp: Mapped[str] = mapped_column(String(18), nullable=False)
    turno: Mapped[str] = mapped_column(String(255), nullable=False)
    generacion: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relaciones
    id_carrera: Mapped[int] = mapped_column(ForeignKey("carreras.id_carrera"), nullable=False)
    carrera: Mapped["Carrera"] = relationship("Carrera", back_populates="alumnos") #type: ignore
    
    grupos: Mapped[list["Grupo"]] = relationship(secondary=grupo_alumnos, back_populates="alumnos") #type: ignore
