from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MetricsService:
    # SQL Queries como constantes de clase
    QUARTERLY_HIRING_QUERY = """
        SELECT 
            d.department,
            j.job,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 1 THEN 1 END) as Q1,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 2 THEN 1 END) as Q2,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 3 THEN 1 END) as Q3,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 4 THEN 1 END) as Q4
        FROM hired_employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE EXTRACT(YEAR FROM datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
    """
    
    DEPARTMENTS_ABOVE_MEAN_QUERY = """
        WITH hired_by_department AS (
            SELECT 
                d.id,
                d.department,
                COUNT(*) as hired
            FROM hired_employees e
            JOIN departments d ON e.department_id = d.id
            WHERE EXTRACT(YEAR FROM datetime) = 2021
            GROUP BY d.id, d.department
        ),
        avg_hired AS (
            SELECT AVG(hired) as mean_hired
            FROM hired_by_department
        )
        SELECT 
            id,
            department,
            hired
        FROM hired_by_department
        WHERE hired > (SELECT mean_hired FROM avg_hired)
        ORDER BY hired DESC;
    """
    
    async def get_quarterly_hiring(self, db: Session) -> Dict[str, Any]:
        """Obtener métricas trimestrales de contratación"""
        try:
            result = db.execute(text(self.QUARTERLY_HIRING_QUERY)).all()

            return {
                "headers": ["department", "job", "Q1", "Q2", "Q3", "Q4"],
                "rows": [
                    {
                        "department": row[0],
                        "job": row[1],
                        "Q1": row[2] or 0,
                        "Q2": row[3] or 0,
                        "Q3": row[4] or 0,
                        "Q4": row[5] or 0
                    }
                    for row in result
                ]
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas trimestrales: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "Error retrieving quarterly hiring metrics", "details": str(e)}
            )
    
    async def get_departments_above_mean(self, db: Session) -> Dict[str, Any]:
        """Obtener departamentos sobre la media de contratación"""
        try:
            result = db.execute(text(self.DEPARTMENTS_ABOVE_MEAN_QUERY)).all()

            return {
                "headers": ["id", "department", "hired"],
                "rows": [
                    {
                        "id": row[0],
                        "department": row[1],
                        "hired": row[2]
                    }
                    for row in result
                ]
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo departamentos sobre la media: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "Error retrieving departments above mean", "details": str(e)}
            )