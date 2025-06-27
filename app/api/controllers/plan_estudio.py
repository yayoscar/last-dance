from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session,lazyload 
from sqlalchemy import select, delete, and_
from app.database.db import get_db_session
from app.database.models.materia import Materia
from app.database.models.plan_estudio import PlanEstudio
from app.database.models.plan_estudio_materia import PlanEstudioMateria  # Ahora es un modelo
from app.api.schemes.planes_estudio_materias import (
    MateriaAsignacion,
    PlanEstudioMateriaAgregar,
    MateriaPlanResponse,
    PlanEstudioConMateriasResponse
)

router = APIRouter()

@router.get("/", response_model=List[PlanEstudioConMateriasResponse])
def listar_planes_estudio(db: Session = Depends(get_db_session)):
    try:
        return db.query(PlanEstudio).options(
            lazyload(PlanEstudio.materias)
        ).all()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id_plan_estudio}/semestres/materias", response_model=Dict[int, List[MateriaPlanResponse]])
def obtener_materias_por_semestre(
    id_plan_estudio: int,
    db: Session = Depends(get_db_session)
):
    plan = db.query(PlanEstudio).filter_by(id_plan_estudio=id_plan_estudio).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")

    # Consulta usando el modelo
    resultados = db.query(PlanEstudioMateria, Materia)\
        .join(Materia, PlanEstudioMateria.id_materia == Materia.id_materia)\
        .filter(PlanEstudioMateria.id_plan_estudio == id_plan_estudio)\
        .all()

    materias_por_semestre = {}
    for relacion, materia in resultados:
        materia_response = MateriaPlanResponse(
            id_materia=materia.id_materia,
            nombre=materia.nombre,
            creditos=materia.creditos,
            tipo=materia.tipo,
            id_modulo=materia.id_modulo,
            semestre=relacion.semestre
        )
        materias_por_semestre.setdefault(relacion.semestre, []).append(materia_response)

    return materias_por_semestre

@router.post("/{id_plan_estudio}/materias", status_code=status.HTTP_201_CREATED)
def asignar_materia_a_semestre(
    id_plan_estudio: int,
    data: MateriaAsignacion,
    db: Session = Depends(get_db_session)
):
    plan = db.query(PlanEstudio).filter_by(id_plan_estudio=id_plan_estudio).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")

    materia = db.query(Materia).filter_by(id_materia=data.id_materia).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    # Verificar si la relación ya existe
    relacion_existente = db.query(PlanEstudioMateria).filter_by(
        id_plan_estudio=id_plan_estudio,
        id_materia=data.id_materia,
        semestre=data.semestre
    ).first()

    if relacion_existente:
        raise HTTPException(status_code=400, detail="La materia ya está asignada a este semestre")

    # Crear la nueva relación usando el modelo
    nueva_relacion = PlanEstudioMateria(
        id_plan_estudio=id_plan_estudio,
        id_materia=data.id_materia,
        semestre=data.semestre
    )
    db.add(nueva_relacion)
    db.commit()

    return {"message": "Materia asignada correctamente"}

@router.delete("/{id_plan_estudio}/materias/{id_materia}", status_code=status.HTTP_204_NO_CONTENT)
def desasignar_materia(
    id_plan_estudio: int,
    id_materia: int,
    semestre: int = Query(..., description="Semestre de la materia a desasignar"),
    db: Session = Depends(get_db_session)
):
    # Eliminar usando el modelo
    relacion = db.query(PlanEstudioMateria).filter_by(
        id_plan_estudio=id_plan_estudio,
        id_materia=id_materia,
        semestre=semestre
    ).first()

    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    db.delete(relacion)
    db.commit()

    return None