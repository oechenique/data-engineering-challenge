from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import pandas as pd
import logging
import os
from typing import Dict, Any
from ..models import Department
from ..utils.validators import validate_file_size, validate_csv_format

logger = logging.getLogger(__name__)

class DepartmentService:
    def __init__(self):
        self.columns = ["id", "department"]

    async def process_upload(self, file: UploadFile, db: Session) -> Dict[str, Any]:
        """Procesar archivo de departamentos sin romper el proceso por duplicados"""
        try:
            await validate_file_size(file)
            await validate_csv_format(file)

            # Estadísticas del proceso
            stats = {
                "total_records": 0,
                "inserted": 0,
                "duplicates": 0,
                "errors": 0,
                "error_details": []
            }

            # Leer CSV sin headers
            try:
                df = pd.read_csv(
                    file.file,
                    header=None,
                    names=self.columns,
                    dtype={"id": "Int64", "department": str}
                )
            except Exception as e:
                logger.error(f"Error leyendo el archivo CSV: {e}")
                raise HTTPException(status_code=400, detail="Archivo CSV inválido")

            stats["total_records"] = len(df)
            logger.info(f"Procesando {stats['total_records']} registros")

            # Obtener IDs existentes en una sola consulta para evitar múltiples queries
            existing_ids = {dept.id for dept in db.query(Department.id).all()}

            # Procesar cada registro
            for _, row in df.iterrows():
                try:
                    # Validar datos requeridos
                    if pd.isna(row['id']) or pd.isna(row['department']):
                        stats["errors"] += 1
                        stats["error_details"].append(f"Datos incompletos en registro: {row.to_dict()}")
                        continue

                    row_id = int(row["id"])

                    # Verificar duplicados antes de insertar
                    if row_id in existing_ids:
                        stats["duplicates"] += 1
                        continue

                    # Crear nuevo departamento
                    department = Department(
                        id=row_id,
                        department=row["department"].strip()
                    )
                    db.add(department)
                    stats["inserted"] += 1

                except Exception as e:
                    stats["errors"] += 1
                    error_msg = f"Error en registro {row.get('id', 'Desconocido')}: {str(e)}"
                    stats["error_details"].append(error_msg)
                    logger.error(error_msg)
                    continue

            # Commit final solo si se insertaron registros nuevos
            if stats["inserted"] > 0:
                try:
                    db.commit()
                except IntegrityError as e:
                    db.rollback()
                    logger.error(f"Error de integridad en la base de datos: {e}")
                    raise HTTPException(status_code=400, detail="Error de integridad en los datos")
                except Exception as e:
                    db.rollback()
                    logger.error(f"Error en commit final: {e}")
                    raise HTTPException(status_code=500, detail="Error guardando los datos")

            return {
                "message": "Proceso completado",
                "summary": {
                    "total_procesados": stats["total_records"],
                    "insertados": stats["inserted"],
                    "duplicados": stats["duplicates"],
                    "errores": stats["errors"],
                    "detalles_errores": stats["error_details"][:5]  # Limitar a 5 errores
                }
            }

        except Exception as e:
            logger.error(f"Error en el proceso: {e}")
            raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")