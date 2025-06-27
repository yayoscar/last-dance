from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status, Query,Response
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, and_,text
from app.database.db import get_db_session
from app.database.models.materia import Materia
from app.database.models.plan_estudio import PlanEstudio
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from app.database.models.plan_estudio_materia import PlanEstudioMateria  # Ahora es un modelo
from app.api.schemes.planes_estudio_materias import (
    MateriaAsignacion,
    PlanEstudioMateriaAgregar,
    MateriaPlanResponse,
    PlanEstudioConMateriasResponse
)
from app.api.schemes.plan_estudio import (
    PlanResponse,
    PlanCrear
)

router = APIRouter()

@router.post("/planes_estudio/", status_code=status.HTTP_201_CREATED, response_model=PlanResponse)
def crear_plan_estudio(
    plan_data: PlanCrear,
    db: Session = Depends(get_db_session)
):
    try:
        nuevo_plan = PlanEstudio(**plan_data.dict())
        db.add(nuevo_plan)
        db.commit()
        db.refresh(nuevo_plan)
        return nuevo_plan
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/planes_estudio/{id_plan_estudio}/semestres/materias", response_model=Dict[int, List[MateriaPlanResponse]])
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

@router.post("/planes_estudio/{id_plan_estudio}/materias", status_code=status.HTTP_201_CREATED)
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

@router.delete("/planes_estudio/{id_plan_estudio}/materias/{id_materia}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.get("/planes_estudio/{id_plan_estudio}/reporte-calificaciones")
def generar_reporte_calificaciones(
    id_plan_estudio: int,
    db: Session = Depends(get_db_session)
):
    try:
        # 1. Verificar si el plan existe
        plan = db.query(PlanEstudio).filter(PlanEstudio.id_plan_estudio == id_plan_estudio).first()
        if not plan:
            return Response(
                content="Plan de estudio no encontrado",
                status_code=404
            )

        # 2. Consulta modificada para ser más tolerante
        query = text("""
        SELECT 
            a.nombre as alumno,
            m.nombre as materia,
            pe.semestre,
            COALESCE(c.parcial_1, 0) as parcial_1,
            COALESCE(c.parcial_2, 0) as parcial_2,
            COALESCE(c.parcial_3, 0) as parcial_3,
            COALESCE(c.final, c.parcial_final, 0) as final
        FROM alumnos a
        JOIN calificaciones c ON a.id_alumno = c.id_alumno
        JOIN materias m ON c.id_materia = m.id_materia
        JOIN plan_estudio_materia pe ON m.id_materia = pe.id_materia
        WHERE pe.id_plan_estudio = :id_plan
        ORDER BY pe.semestre, m.nombre, a.nombre
        """)

        result = db.execute(query, {"id_plan": id_plan_estudio})
        rows = result.mappings().all()

        if not rows:
            return Response(
                content="No hay calificaciones registradas para este plan",
                status_code=404
            )

        # 3. Crear DataFrame
        df = pd.DataFrame(rows)

        # 4. Generar Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Calificaciones', index=False)
        
        output.seek(0)

        # 5. Retornar archivo
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=calificaciones_plan_{id_plan_estudio}.xlsx"}
        )

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar reporte: {str(e)}"
        )