from app.database.db import Base
from sqlalchemy import Column, ForeignKey,  Table

grupo_alumnos = Table(
    "grupo_alumnos",
    Base.metadata,
    Column("id_grupo", ForeignKey("grupos.id_grupo"), primary_key=True),
    Column("id_alumno", ForeignKey("alumnos.id_alumno"), primary_key=True),
)