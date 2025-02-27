from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemes import materias
from app.api.schemes.materias import MateriaCrear, MateriaEditar, MateriaResponse
from app.database.db import get_db_session
from app.database.models import materia
from app.database.models.materia import Materia


router = APIRouter()

@router.post("/",response_model=MateriaResponse)
def crear_materia(materia: MateriaCrear,db: Session = Depends(get_db_session)):
    db_materia=Materia(**materia.model_dump())
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

@router.get("/",response_model=List[MateriaResponse])
def obtener_materias(db: Session = Depends(get_db_session)):
    return db.query(Materia).all()

#GET /{id_materia}
@router.get("/{id}", response_model=MateriaResponse)
def obtener_item(id: int,db: Session = Depends(get_db_session)):
    materia = db.query(Materia).filter_by(id_materia=id).first()
    return materia

#Patch /{id_materia}
@router.patch("/{id}", response_model=MateriaResponse)
def editar_item(id: int, materia:MateriaEditar,db: Session = Depends(get_db_session)):
    db_materia= db.query(Materia).filter_by(id_materia=id).first()
    db_materia.nombre = materia.nombre
    db.commit()
    db.refresh(db_materia)
    return db_materia
    
#DElETE /{id_materia}
@router.delete("/{id}")
def eliminar_item(id: int,db: Session = Depends(get_db_session)):
    db_materia = db.query(Materia).filter_by(id_materia=id).first()
    db.delete(db_materia)
    db.commit()
    return {"message":"Materia eliminada"}
