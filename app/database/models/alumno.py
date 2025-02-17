from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base
from sqlalchemy import String, Boolean, BigInteger, ForeignKey, Integer

class Alumno(Base):
    __tablename__ = "alumnos"

    id_alumno: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ape_paterno: Mapped[str] = mapped_column(String(255), nullable=False)
    ape_materno: Mapped[str] = mapped_column(String(255), nullable=False)
    num_control: Mapped[int] = mapped_column(Integer, nullable=False)
    curp: Mapped[str] = mapped_column(String(18), nullable=False)
    id_carrera: Mapped[int] = mapped_column(ForeignKey("carreras.id_carrera"), nullable=False)
    turno: Mapped[str] = mapped_column(String(255), nullable=False)
    local: Mapped[bool] = mapped_column(Boolean, nullable=False)
    generacion: Mapped[int] = mapped_column(BigInteger, nullable=False)
