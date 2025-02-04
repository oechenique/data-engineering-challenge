from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.department_service import DepartmentService

router = APIRouter(tags=["departments"])

@router.post("/upload/departments")
async def upload_departments(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)  # ✅ YA FUNCIONA DIRECTO, sin `next(db_generator)`
):
    """
    Cargar departamentos desde CSV
    
    Args:
        file: Archivo CSV con datos de departamentos
        db: Sesión de base de datos
        
    Returns:
        dict: Resumen del proceso
    """
    department_service = DepartmentService()
    return await department_service.process_upload(file, db)