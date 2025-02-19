from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.api.schemes.carrera import CarreraSchema
from app.database.db import get_db_session


from app.database.models.carrera import Carrera


router = APIRouter()

@router.post("/",response_model=CarreraSchema)
def crear_carrera(carrera: CarreraSchema,db: Session = Depends(get_db_session)):
    db_carrera = Carrera(**carrera.model_dump(exclude_unset=True, exclude_none=True))
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

@router.get("/",response_model=List[CarreraSchema])
def obtener_carreras(db: Session = Depends(get_db_session)):
    return db.query(Carrera).all()


