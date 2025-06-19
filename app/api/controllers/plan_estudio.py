from typing import Dict, List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session,lazyload ,joinedload
from sqlalchemy import select, delete, and_
from app.database.db import get_db_session
from app.database.models.carrera import Carrera
from app.database.models.materia import Materia
from app.database.models.plan_estudio import PlanEstudio
from app.api.schemes.plan_estudio import (PlanCrear, PlanEditar, PlanResponse)
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
    
# Asegúrate que tus rutas estén consistentes con o sin barra final
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_plan_estudio(plan_data: PlanCrear, db: Session = Depends(get_db_session)):
        try:
            nuevo_plan = PlanEstudio(**plan_data.dict())
            db.add(nuevo_plan)
            db.commit()
            db.refresh(nuevo_plan)
            return nuevo_plan
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=PlanResponse)
def crear_plan(plan: PlanCrear, db: Session = Depends(get_db_session)):
    # Verificar que la carrera existe
    carrera = db.query(Carrera).filter_by(id_carrera=plan.id_carrera).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    db_plan = PlanEstudio(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    # Cargar la relación con carrera
    db_plan_with_carrera = db.query(PlanEstudio).options(
        joinedload(PlanEstudio.carrera)
    ).filter_by(id_plan_estudio=db_plan.id_plan_estudio).first()
    
    return db_plan_with_carrera

@router.get("/", response_model=List[PlanResponse])
def obtener_planes(db: Session = Depends(get_db_session)):
    planes = db.query(PlanEstudio).options(
        joinedload(PlanEstudio.carrera)
    ).all()
    return planes

@router.get("/{id}", response_model=PlanResponse)
def obtener_plan(id: int, db: Session = Depends(get_db_session)):
    plan = db.query(PlanEstudio).options(
        joinedload(PlanEstudio.carrera)
    ).filter_by(id_plan_estudio=id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")
    
    return plan

@router.patch("/{id}", response_model=PlanResponse)
def editar_plan(id: int, plan_data: PlanEditar, db: Session = Depends(get_db_session)):
    # Verificar que el plan existe
    db_plan = db.query(PlanEstudio).filter_by(id_plan_estudio=id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")
    
    # Verificar que la carrera existe
    carrera = db.query(Carrera).filter_by(id_carrera=plan_data.id_carrera).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    # Actualizar campos
    db_plan.nombre = plan_data.nombre
    db_plan.id_carrera = plan_data.id_carrera
    
    db.commit()
    db.refresh(db_plan)
    
    # Cargar la relación con carrera
    db_plan_with_carrera = db.query(PlanEstudio).options(
        joinedload(PlanEstudio.carrera)
    ).filter_by(id_plan_estudio=db_plan.id_plan_estudio).first()
    
    return db_plan_with_carrera

@router.delete("/{id}")
def eliminar_plan(id: int, db: Session = Depends(get_db_session)):
    db_plan = db.query(PlanEstudio).filter_by(id_plan_estudio=id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")
    
    db.delete(db_plan)
    db.commit()
    return {"message": "Plan de estudio eliminado"}

@router.post("/pdf/")
async def subida_pdf(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(await file.read())
    }

@router.post("/{id_plan_estudio}/agregar-materias")
def agregar_materias_a_plan(id_plan_estudio: int, data: PlanEstudioMateriaAgregar, db: Session = Depends(get_db_session)):
    # Verificar existencia del plan
    plan_estudio = db.query(PlanEstudio).filter_by(id_plan_estudio=id_plan_estudio).first()
    if not plan_estudio:
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