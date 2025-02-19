from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemes.alumno import AlumnoResponse,AlumnoCrear
from app.database.db import get_db_session
from app.database.models.alumno import Alumno

router = APIRouter()



@router.post("/", response_model=AlumnoResponse)
def crear_alumno(alumno: AlumnoCrear, db: Session = Depends(get_db_session)):
    alumno_data = alumno.model_dump(exclude={"id_alumno"})  # 🔥 Excluye id_alumno del request
    db_alumno = Alumno(**alumno_data)
    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)
    return db_alumno

@router.get("/", response_model=List[AlumnoResponse])
def obtener_alumnso(db: Session = Depends(get_db_session)):
    return db.query(Alumno).all()


    
