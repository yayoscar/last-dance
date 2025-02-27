from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemes.alumno import AlumnoResponse, AlumnoCrear, AlumnoEditar  # Asegúrate de importar AlumnoEditar
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
def obtener_alumnos(db: Session = Depends(get_db_session)):
    return db.query(Alumno).all()

@router.get("/{id}", response_model=AlumnoResponse)
def obtener_item(id: int, db: Session = Depends(get_db_session)):
    carrera = db.query(Alumno).filter_by(id_carrera=id).first()
    return Alumno

@router.post("/", response_model=AlumnoResponse)
def crear_carrera(carrera: AlumnoCrear, db: Session = Depends(get_db_session)):
    db_carrera = Alumno(**carrera.model_dump())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

@router.patch("/{id}", response_model=AlumnoResponse)
def editar_item(id: int, alumno: AlumnoEditar, db: Session = Depends(get_db_session)):  # type: ignore
    db_carrera = db.query(Alumno).filter_by(id_carrera=id).first()
    db_carrera.nombre = alumno.nombre
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

#DElETE /{id_carrera}
@router.delete("/{id}")
def eliminar_item(id: int,db: Session = Depends(get_db_session)):
    db_alumno = db.query(Alumno).filter_by(id_alumno=id).first()
    db.delete(db_alumno)
    db.commit()
    return {"message":"Carrera eliminada"}