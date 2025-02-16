from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base
from sqlalchemy import String

class PlanEstudio(Base):
    __tablename__ = "planes_estudio"

    id_plan_estudio: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)