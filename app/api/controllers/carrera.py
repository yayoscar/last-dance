from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.schemes.carrera import CarreraCrear, CarreraResponse
from app.database.db import get_db_session
from app.database.models.carrera import Carrera


router = APIRouter()

@router.post("/",response_model=CarreraResponse)
def crear_carrera(carrera: CarreraCrear,db: Session = Depends(get_db_session)):
    db_carrera=Carrera(**carrera.model_dump())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

@router.get("/",response_model=List[CarreraResponse])
def obtener_carreras(db: Session = Depends(get_db_session)):
    return db.query(Carrera).all()

#GET /{id_carrera}
@router.get("/{id}", response_model=CarreraResponse)
def obtener_item(id: int,db: Session = Depends(get_db_session)):
    carrera = db.query(Carrera).filter_by(id_carrera=id).first()
    return carrera

    

#PATCH /{id_carrera}

#DElETE /{id_carrera}
