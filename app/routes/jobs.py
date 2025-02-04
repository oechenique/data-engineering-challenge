from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.job_service import JobService

router = APIRouter(tags=["jobs"])

@router.post("/upload/jobs")
async def upload_jobs(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Cargar trabajos desde CSV
    
    Args:
        file: Archivo CSV con datos de trabajos
        db: Sesión de base de datos
        
    Returns:
        dict: Resumen del proceso
    """
    job_service = JobService()
    return await job_service.process_upload(file, db)