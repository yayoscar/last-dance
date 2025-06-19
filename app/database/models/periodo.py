from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database.db import Base
from sqlalchemy import String, Date

class Periodo(Base):
    __tablename__ = "periodos"

    id_periodo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    
    grupos : Mapped[list["Grupo"]] = relationship("Grupo", back_populates="periodo") #type: ignore
