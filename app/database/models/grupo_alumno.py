from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base
from sqlalchemy import String, ForeignKey, Integer

class GrupoAlumno(Base):
    __tablename__ = "grupo_alumnos"

    id_grupo_alumno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_grupo: Mapped[int] = mapped_column(ForeignKey("grupos.id_grupo"), nullable=False)
    id_alumno: Mapped[int] = mapped_column(ForeignKey("alumnos.id_alumno"), nullable=False)
    tipo_inscripcion: Mapped[str | None] = mapped_column(String(255))
