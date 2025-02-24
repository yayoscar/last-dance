from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemes import carrera
from app.api.schemes.carrera import CarreraCrear, CarreraEditar, CarreraResponse
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

#Patch /{id_carrera}
@router.patch("/{id}", response_model=CarreraResponse)
def editar_item(id: int, carrera:CarreraEditar,db: Session = Depends(get_db_session)):
    db_carrera = db.query(Carrera).filter_by(id_carrera=id).first()
    db_carrera.nombre = carrera.nombre
    db.commit()
    db.refresh(db_carrera)
    return db_carrera
    
#DElETE /{id_carrera}
@router.delete("/{id}")
def eliminar_item(id: int,db: Session = Depends(get_db_session)):
    db_carrera = db.query(Carrera).filter_by(id_carrera=id).first()
    db.delete(db_carrera)
    db.commit()
    return {"message":"Carrera eliminada"}
