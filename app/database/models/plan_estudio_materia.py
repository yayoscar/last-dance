from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

plan_estudio_materias = Table(
    "plan_estudio_materias",
    Base.metadata,
    Column("id_plan_estudio", ForeignKey("planes_estudio.id_plan_estudio"), primary_key=True),
    Column("id_materia", ForeignKey("materias.id_materia"), primary_key=True),
    Column("semestre", Integer, nullable=False),
)