from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.schemes.materias import MateriaCrear, MateriaEditar, MateriaResponse, TipoMateria
from app.database.db import get_db_session
from app.database.models.materia import Materia

router = APIRouter()

@router.post("/", response_model=MateriaResponse, status_code=status.HTTP_201_CREATED)
async def crear_materia(materia_data: MateriaCrear, db: Session = Depends(get_db_session)):
    # Validar que si es tipo "Módulo" tenga un módulo seleccionado
    if materia_data.tipo == "Módulo" and materia_data.id_modulo is None:
        raise HTTPException(
            status_code=400, 
            detail="id_modulo es requerido para materias de tipo Módulo"
        )
    
    # Validar que si es tipo "Materia" no tenga módulo
    if materia_data.tipo == "Materia" and materia_data.id_modulo is not None:
        raise HTTPException(
            status_code=400,
            detail="Las materias de tipo Materia no pueden tener módulo asociado"
        )
    
    nueva_materia = Materia(**materia_data.dict())
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia


@router.get("/", response_model=List[MateriaResponse])
def obtener_materias(db: Session = Depends(get_db_session)):
    return db.query(Materia).all()

@router.get("/{id}", response_model=MateriaResponse)
def obtener_item(id: int, db: Session = Depends(get_db_session)):
    db_materia = db.query(Materia).filter_by(id_materia=id).first()
    if not db_materia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    return db_materia

@router.patch("/{id}", response_model=MateriaResponse)
def editar_item(id: int, materia: MateriaEditar, db: Session = Depends(get_db_session)):
    db_materia = db.query(Materia).filter_by(id_materia=id).first()
    if not db_materia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    
    update_data = materia.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_materia, field, value)
    
    db.commit()
    db.refresh(db_materia)
    return db_materia
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_item(id: int, db: Session = Depends(get_db_session)):
    db_materia = db.query(Materia).filter_by(id_materia=id).first()
    if not db_materia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    
    db.delete(db_materia)
    db.commit()
    return None  # 204 responses should have no content