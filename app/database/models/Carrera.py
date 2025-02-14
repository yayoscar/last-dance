from sqlalchemy import Column, Integer, String

from app.database.config import Base


class Carrera(Base):
    __tablename__="carreras"
    id_carrera = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)