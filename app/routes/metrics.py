from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.metrics_service import MetricsService

router = APIRouter(tags=["metrics"])

@router.get("/quarterly-hiring")
async def get_quarterly_hiring(db: Session = Depends(get_db)):
    """Obtener métricas trimestrales de contratación"""
    metrics_service = MetricsService()
    return await metrics_service.get_quarterly_hiring(db)

@router.get("/departments-above-mean")
async def get_departments_above_mean(db: Session = Depends(get_db)):
    """Obtener departamentos sobre la media de contratación"""
    metrics_service = MetricsService()
    return await metrics_service.get_departments_above_mean(db)