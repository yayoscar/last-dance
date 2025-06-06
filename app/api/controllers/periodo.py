from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db_session
from app.database.models.periodo import Periodo
from app.api.schemes.periodo import PeriodoCrear, PeriodoEditar, PeriodoResponse

router = APIRouter()

@router.post("/", response_model=PeriodoResponse)
def crear_periodo(periodo: PeriodoCrear, db: Session = Depends(get_db_session)):
    db_periodo = Periodo(**periodo.model_dump())
    db.add(db_periodo)
    db.commit()
    db.refresh(db_periodo)
    return db_periodo

@router.get("/", response_model=List[PeriodoResponse])
def obtener_periodos(db: Session = Depends(get_db_session)):
    return db.query(Periodo).all()

@router.get("/{id_periodo}", response_model=PeriodoResponse)
def obtener_periodo(id_periodo: int, db: Session = Depends(get_db_session)):
    periodo = db.query(Periodo).filter_by(id_periodo=id_periodo).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return periodo

@router.patch("/{id_periodo}", response_model=PeriodoResponse)
def editar_periodo(id_periodo: int, periodo: PeriodoEditar, db: Session = Depends(get_db_session)):
    db_periodo = db.query(Periodo).filter_by(id_periodo=id_periodo).first()
    if not db_periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")

    for attr, value in periodo.model_dump(exclude_unset=True).items():
        setattr(db_periodo, attr, value)

    db.commit()
    db.refresh(db_periodo)
    return db_periodo

@router.delete("/{id_periodo}")
def eliminar_periodo(id_periodo: int, db: Session = Depends(get_db_session)):
    db_periodo = db.query(Periodo).filter_by(id_periodo=id_periodo).first()
    if not db_periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    db.delete(db_periodo)
    db.commit()
    return {"message": "Periodo eliminado correctamente"}
