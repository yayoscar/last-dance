from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.api.schemes import plan_estudio
from app.api.schemes.plan_estudio import PlanCrear, PlanEditar, PlanResponse
from app.database.db import get_db_session
from app.database.models.plan_estudio import PlanEstudio


router = APIRouter()

@router.post("/",response_model=PlanResponse)
def crear_plan(plan: PlanCrear,db: Session = Depends(get_db_session)):
    db_plan=PlanEstudio(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get("/",response_model=List[PlanResponse])
def obtener_plan(db: Session = Depends(get_db_session)):
    return db.query(PlanEstudio).all()

#GET /{id_plan}
@router.get("/{id}", response_model=PlanResponse)
def obtener_item(id: int,db: Session = Depends(get_db_session)):
    plan = db.query(PlanEstudio).filter_by(id_plan=id).first()
    return plan

#Patch /{id_plan}
@router.patch("/{id}", response_model=PlanResponse)
def editar_item(id: int, plan:PlanEditar,db: Session = Depends(get_db_session)):
    db_plan_estudio= db.query(plan).filter_by(id_plan=id).first()
    db_plan_estudio.nombre = plan_estudio.nombre
    db.commit()
    db.refresh(db_plan_estudio)
    return db_plan_estudio
    
#DElETE /{id_plan}
@router.delete("/{id}")
def eliminar_item(id: int,db: Session = Depends(get_db_session)):
    db_plan = db.query(plan_estudio).filter_by(id_plan=id).first()
    db.delete(db_plan)
    db.commit()
    return {"message":"Plan eliminada"}

from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@router.post("/pdf/")
async def subida_pdf(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(await file.read())
    }
