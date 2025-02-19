from __future__ import annotations
import datetime
from app.core import settings

from sqlalchemy import DateTime,create_engine
from typing import Generator
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    """Base class for all models"""

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    } 
    


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
) 

# 📌 Crear sessionmaker para sesiones síncronas
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 📌 Dependencia para obtener la sesión síncrona
def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()