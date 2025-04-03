from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/pdf/")
async def subida_pdf(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(await file.read()) 
    }