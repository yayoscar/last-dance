from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.config import Base


class Alumno(Base):
    __tablename__ = "alumnos"
    id_alumno = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    ape_paterno = Column(String(255), nullable=False)
    ape_materno = Column(String(255), nullable=False)
    num_control = Column(Integer, nullable=False)
    curp = Column(String(255), nullable=False)
    id_carrera = Column(Integer, ForeignKey("carreras.id_carrera"))
    turno = Column(String(255), nullable=False)
    local = Column(Boolean, nullable=False)
    generacion = Column(Integer, nullable=False)

    carrera = relationship("Carrera")