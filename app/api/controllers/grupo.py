from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert, join, select
from sqlalchemy.orm import Session, joinedload
from app.api.schemes.grupo import (
    AlumnoGrupoResponse, 
    GrupoCrear, 
    GrupoEditar, 
    GrupoConAlumnosResponse, 
    GrupoAlumnoAgregar, 
    GrupoResponse
)
from app.database.db import get_db_session
from app.database.models.periodo import Periodo
from app.database.models.alumno import Alumno
from app.database.models.grupo import Grupo
from app.database.models.grupo_alumno import grupo_alumnos

router = APIRouter()

@router.post("/", response_model=GrupoResponse)
def crear_grupo(grupo: GrupoCrear, db: Session = Depends(get_db_session)):
    # Verificar que el plan existe
    periodos = db.query(Periodo).filter_by(id_periodos=grupo.id_carrera).first()
    if not periodos:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    
    db_grupo = Grupo(**grupo.model_dump())
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    
    # Cargar la relación con periodos
    db_grupo_with_periodos = db.query(Grupo).options(
        joinedload(Grupo.periodos)
    ).filter_by(id_grupo=db_grupo.id_grupo).first()
    
    return db_grupo_with_periodos

@router.get("/", response_model=List[GrupoResponse])
def obtener_grupos(db: Session = Depends(get_db_session)):
    grupo = db.query(Grupo).options(
        joinedload(Grupo.periodo)
    ).all()
    return grupo

@router.get("/{id}", response_model=GrupoResponse)
def obtener_grupo(id: int, db: Session = Depends(get_db_session)):
    grupo = db.query(Grupo).options(
        joinedload(Grupo.periodo)
    ).filter_by(id_grupo=id).first()
    
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    return grupo

@router.patch("/{id}", response_model=GrupoResponse)
def editar_grupo(id: int, grupo_data: GrupoEditar, db: Session = Depends(get_db_session)):
    # Verificar que el grupo existe
    db_grupo = db.query(Grupo).filter_by(id_grupo=id).first()
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    # Verificar que el periodo existe
    periodo = db.query(Periodo).filter_by(id_periodo=grupo_data.id_periodo).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    
    # Actualizar campos
    db_grupo.nombre = grupo_data.nombre
    db_grupo.id_carrera = grupo_data.id_periodo
    
    db.commit()
    db.refresh(db_grupo)
    
    # Cargar la relación con periodo
    db_grupo_with_periodo = db.query(Grupo).options(
        joinedload(Grupo.periodo)
    ).filter_by(id_grupo=db_grupo.id_grupo).first()
    
    return db_grupo_with_periodo

@router.delete("/{id}")
def eliminar_grupo(id: int, db: Session = Depends(get_db_session)):
    db_grupo = db.query(Grupo).filter_by(id_grupo=id).first()
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    db.delete(db_grupo)
    db.commit()
    return {"message": "Grupo eliminado"}


@router.post("/{id_grupo}/agregar-periodos")
def agregar_periodos_a_grupo(id_grupo: int, data: GrupoAlumnoAgregar, db: Session = Depends(get_db_session)):
    # Verificar existencia del grupo
    grupo = db.query(Grupo).filter_by(id_grupo=id_grupo).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    # Verificar que todas los carrera existen
    ids_alumnos = [m.id_alumnos for m in data.alumnos]
    alumnos_existentes = db.query(Alumno).filter(Alumno.id_materia.in_(ids_alumnos)).all()
    if len(alumnos_existentes) != len(ids_alumnos):
        raise HTTPException(status_code=400, detail="Una o más alumnos no existen")

    # Insertar relaciones
    insert_data = [
        {
            "id_grupo": id_grupo,
            "id_alumno": m.id_alumno,
            "semestre": m.semestre
        }
        for m in data.alumnos
    ]

    db.execute(insert(grupo_alumnos), insert_data)
    db.commit()

    return {"message": f"{len(insert_data)} alumnos agregados al grupo"}

@router.get("/{id_grupo}/con-alumnos", response_model=GrupoConAlumnosResponse)
def obtener_grupos_con_alumnos(id_grupo: int, db: Session = Depends(get_db_session)):
    # Obtener el grupo con su periodo
    grupo = db.query(Grupo).options(
        joinedload(Grupo.periodo)
    ).filter_by(id_grupo=id_grupo).first()
    
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    # Obtener las materias del plan
    stmt = (
        select(
            Alumno.id_alumno,
            Alumno.nombre,
            Alumno.ape_paterno,
            Alumno.ape_materno,
            Alumno.num_control,
            Alumno.curp,
            Alumno.turno,
            Alumno.generacion,
            grupo_alumnos.c.semestre
        )
        .select_from(
            join(
                grupo_alumnos,
                Alumno,
                grupo_alumnos.c.id_alumno == Alumno.id_alumno
            )
        )
        .where(grupo_alumnos.c.id_grupo == id_grupo)
    )

    alumnos = db.execute(stmt).fetchall()

    alumnos_response = [
        AlumnoGrupoResponse(
            id_alumno=row.id_alumno,
            nombre=row.nombre,
            ape_paterno=row.ape_paterno,
            ape_materno=row.ape_materno,
            num_control=row.num_control,
            curp=row.curp,
            turno=row.turno,
            generacion=row.generacion,
            semestre=row.semestre
        )
        for row in alumnos
    ]

    return GrupoConAlumnosResponse(
        id_grupo=grupo.id_grupo,
        nombre=grupo.nombre,
        id_periodo=grupo.id_periodo,
        periodo=grupo.periodo,
        alumno=alumnos_response
    )