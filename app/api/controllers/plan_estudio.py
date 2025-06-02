from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert, join, select
from sqlalchemy.orm import Session, joinedload
from app.api.schemes.plan_estudio import (
    MateriaPlanResponse, 
    PlanCrear, 
    PlanEditar, 
    PlanEstudioConMateriasResponse, 
    PlanEstudioMateriaAgregar, 
    PlanResponse
)
from app.database.db import get_db_session
from app.database.models.carrera import Carrera
from app.database.models.materia import Materia
from app.database.models.plan_estudio import PlanEstudio
from app.database.models.plan_estudio_materia import plan_estudio_materias

router = APIRouter()

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

    # Verificar que todas las materias existen
    ids_materias = [m.id_materia for m in data.materias]
    materias_existentes = db.query(Materia).filter(Materia.id_materia.in_(ids_materias)).all()
    if len(materias_existentes) != len(ids_materias):
        raise HTTPException(status_code=400, detail="Una o más materias no existen")

    # Insertar relaciones
    insert_data = [
        {
            "id_plan_estudio": id_plan_estudio,
            "id_materia": m.id_materia,
            "semestre": m.semestre
        }
        for m in data.materias
    ]

    db.execute(insert(plan_estudio_materias), insert_data)
    db.commit()

    return {"message": f"{len(insert_data)} materias agregadas al plan de estudio"}

@router.get("/{id_plan_estudio}/con-materias", response_model=PlanEstudioConMateriasResponse)
def obtener_plan_con_materias(id_plan_estudio: int, db: Session = Depends(get_db_session)):
    # Obtener el plan con su carrera
    plan = db.query(PlanEstudio).options(
        joinedload(PlanEstudio.carrera)
    ).filter_by(id_plan_estudio=id_plan_estudio).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")

    # Obtener las materias del plan
    stmt = (
        select(
            Materia.id_materia,
            Materia.nombre,
            Materia.creditos,
            Materia.tipo,
            Materia.id_modulo,
            plan_estudio_materias.c.semestre
        )
        .select_from(
            join(
                plan_estudio_materias,
                Materia,
                plan_estudio_materias.c.id_materia == Materia.id_materia
            )
        )
        .where(plan_estudio_materias.c.id_plan_estudio == id_plan_estudio)
    )

    materias = db.execute(stmt).fetchall()

    materias_response = [
        MateriaPlanResponse(
            id_materia=row.id_materia,
            nombre=row.nombre,
            creditos=row.creditos,
            tipo=row.tipo,
            id_modulo=row.id_modulo,
            semestre=row.semestre
        )
        for row in materias
    ]

    return PlanEstudioConMateriasResponse(
        id_plan_estudio=plan.id_plan_estudio,
        nombre=plan.nombre,
        id_carrera=plan.id_carrera,
        carrera=plan.carrera,
        materias=materias_response
    )