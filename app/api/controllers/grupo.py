from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemes.grupo import GrupoResponse, GrupoCrear, GrupoEditar  # Asegúrate de importar AlumnoEditar
from app.database.db import get_db_session
from app.database.models.grupo import Grupo
from fastapi.responses import FileResponse
import pandas as pd
from openpyxl import Workbook
from tempfile import NamedTemporaryFile

router = APIRouter()

@router.post("/", response_model=GrupoResponse)
def crear_grupo(grupo: GrupoCrear, db: Session = Depends(get_db_session)):
    db_grupo = Grupo(**grupo.model_dump())
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.get("/", response_model=List[GrupoResponse])
def obtener_grupos(db: Session = Depends(get_db_session)):
    return db.query(Grupo).all()

@router.get("/{id_grupo}", response_model=GrupoResponse)
def obtener_grupo(id_grupo: int, db: Session = Depends(get_db_session)):
    grupo = db.query(Grupo).filter_by(id_grupo=id_grupo).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo

@router.patch("/{id_grupo}", response_model=GrupoResponse)
def editar_grupo(id_grupo: int, grupo: GrupoEditar, db: Session = Depends(get_db_session)):
    db_grupo = db.query(Grupo).filter_by(id_grupo=id_grupo).first()
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    for key, value in grupo.model_dump(exclude_unset=True).items():
        setattr(db_grupo, key, value)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.delete("/{id_grupo}")
def eliminar_grupo(id_grupo: int, db: Session = Depends(get_db_session)):
    db_grupo = db.query(Grupo).filter_by(id_grupo=id_grupo).first()
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    db.delete(db_grupo)
    db.commit()
    return {"message": "Grupo eliminado"}

@router.get("/{id_grupo}/plantilla-calificaciones")
def generar_plantilla_calificaciones(id_grupo: int, db: Session = Depends(get_db_session)):
    # 1. Verificar si el grupo existe
    grupo = db.query(Grupo).filter_by(id_grupo=id_grupo).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    # 2. Obtener alumnos del grupo (ajusta según tu modelo de relación)
    alumnos = grupo.alumnos
    
    # 3. Obtener materias del semestre (necesitarás implementar esta relación)
    # materias = grupo.materias  # Ajusta según tu modelo
    
    # 4. Crear estructura de datos para el Excel
    data = []
    for alumno in alumnos:
        row = {
            "Matrícula": alumno.matricula,
            "Nombre": f"{alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}",
            # Agregar más campos según necesites
        }
        
        # Agregar columnas para cada materia
        # for materia in materias:
        #     row[f"{materia.nombre} - Parcial 1"] = ""
        #     row[f"{materia.nombre} - Parcial 2"] = ""
        #     row[f"{materia.nombre} - Parcial 3"] = ""
        #     row[f"{materia.nombre} - Asistencias"] = ""
        
        data.append(row)
    
    # 5. Crear DataFrame y generar Excel
    df = pd.DataFrame(data)
    
    # Crear archivo temporal
    with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        with pd.ExcelWriter(tmp.name, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Calificaciones')
            
            # Formato adicional (opcional)
            workbook = writer.book
            worksheet = writer.sheets['Calificaciones']
            
            # Ajustar ancho de columnas
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # 6. Devolver el archivo
    return FileResponse(
        tmp.name,
        filename=f"Plantilla_Calificaciones_Grupo_{grupo.nombre}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )