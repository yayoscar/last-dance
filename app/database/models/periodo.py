from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database.db import Base
from sqlalchemy import String, Date

class Periodo(Base):
    __tablename__ = "periodos"

    id_periodo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    periodo: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_inicio: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_fin: Mapped[str] = mapped_column(String(50), nullable=False)

    grupos : Mapped[list["Grupo"]] = relationship("Grupo", back_populates="periodo") #type: ignore
