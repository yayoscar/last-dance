from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemes import periodo
from app.api.schemes.periodo import PeriodoCrear, PeriodoEditar, PeriodoResponse
from app.database.db import get_db_session
from app.database.models.periodo import Periodo

router = APIRouter()

@router.post("/",response_model=PeriodoResponse)
def crear_periodo(periodo: PeriodoCrear,db: Session = Depends(get_db_session)):
    db_periodo=Periodo(**periodo.model_dump())
    db.add(db_periodo)
    db.commit()
    db.refresh(db_periodo)
    return db_periodo

@router.get("/",response_model=List[PeriodoResponse])
def obtener_periodos(db: Session = Depends(get_db_session)):
    return db.query(Periodo).all()

#GET /{id_periodo}
@router.get("/{id}", response_model=PeriodoResponse)
def obtener_item(id: int,db: Session = Depends(get_db_session)):
    periodo = db.query(Periodo).filter_by(id_periodo=id).first()
    return periodo

#Patch /{id_periodo}
@router.patch("/{id}", response_model=PeriodoResponse)
def editar_item(id: int, periodo:PeriodoEditar,db: Session = Depends(get_db_session)):
    db_periodo = db.query(Periodo).filter_by(id_periodo=id).first()
    db_periodo.nombre = periodo.nombre
    db.commit()
    db.refresh(db_periodo)
    return db_periodo
    
#DElETE /{id_periodo}
@router.delete("/{id}")
def eliminar_item(id: int,db: Session = Depends(get_db_session)):
    db_periodo = db.query(Periodo).filter_by(id_periodo=id).first()
    db.delete(db_periodo)
    db.commit()
    return {"message":"Periodo eliminado"}
