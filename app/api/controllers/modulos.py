from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db_session
from app.database.models.modulo import Modulo as ModuloModel  # Renombramos para evitar conflicto
from app.api.schemes.modulos import ModuloCreate, Modulo

router = APIRouter()

@router.post("/", response_model=Modulo)
def create_modulo(modulo: ModuloCreate, db: Session = Depends(get_db_session)):
    # Crear instancia del modelo SQLAlchemy directamente
    db_modulo = ModuloModel(nombre=modulo.nombre)
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo  # FastAPI convertirá automáticamente a esquema Pydantic

@router.get("/", response_model=List[Modulo])
def read_modulos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return db.query(ModuloModel).offset(skip).limit(limit).all()
@router.get("/{modulo_id}", response_model=Modulo)
def read_modulo(modulo_id: int, db: Session = Depends(get_db_session)):
    db_modulo = db.query(Modulo).filter(Modulo.id_modulo == modulo_id).first()
    if db_modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return db_modulo

@router.put("/{modulo_id}", response_model=Modulo)
def update_modulo(modulo_id: int, modulo: ModuloCreate, db: Session = Depends(get_db_session)):
    db_modulo = db.query(Modulo).filter(Modulo.id_modulo == modulo_id).first()
    if db_modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    for key, value in modulo.model_dump().items():
        setattr(db_modulo, key, value)
    
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

@router.delete("/{modulo_id}")
def delete_modulo(modulo_id: int, db: Session = Depends(get_db_session)):
    db_modulo = db.query(Modulo).filter(Modulo.id_modulo == modulo_id).first()
    if db_modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    db.delete(db_modulo)
    db.commit()
    return {"message": "Módulo eliminado correctamente"}