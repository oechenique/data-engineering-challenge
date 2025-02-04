from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import logging
from ..database import get_db
from ..services.employee_service import EmployeeService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["employees"])

@router.post("/upload/hired_employees")
async def upload_hired_employees(
    file: UploadFile = File(...),
    update_existing: bool = False,
    db: Session = Depends(get_db)
):
    """
    Cargar empleados desde CSV
    
    Args:
        file: Archivo CSV con datos de empleados
        update_existing: Si actualizar registros existentes
        db: Sesión de base de datos
        
    Returns:
        dict: Resumen del proceso
    """
    employee_service = EmployeeService()
    return await employee_service.process_upload(file, update_existing, db)