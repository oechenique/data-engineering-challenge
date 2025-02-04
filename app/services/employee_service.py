from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import pandas as pd
import logging
from typing import Dict, Any, Set
from ..models import HiredEmployee
from ..utils.validators import validate_file_size, validate_csv_format

logger = logging.getLogger(__name__)

class EmployeeService:
    def __init__(self):
        self.BATCH_SIZE = 1000
        self.columns = ["id", "name", "datetime", "department_id", "job_id"]

    async def process_batch(
        self, 
        batch_df: pd.DataFrame, 
        db: Session, 
        processed_ids: Set[int], 
        errors: list,
        update_existing: bool
    ) -> Set[int]:
        batch_processed_ids = set()
        employees = []
        
        for _, row in batch_df.iterrows():
            if int(row['id']) in processed_ids:
                continue
                
            try:
                employee = HiredEmployee(
                    id=int(row['id']),
                    name=row['name'] if pd.notna(row['name']) else None,
                    datetime=row['datetime'] if pd.notna(row['datetime']) else None,
                    department_id=int(row['department_id']) if pd.notna(row['department_id']) else None,
                    job_id=int(row['job_id']) if pd.notna(row['job_id']) else None
                )
                employees.append(employee)
            except Exception as e:
                errors.append(f"Error processing ID {row.get('id', 'N/A')}: {str(e)}")
                continue

        if employees:
            try:
                if update_existing:
                    for emp in employees:
                        db.merge(emp)
                        db.commit()
                        batch_processed_ids.add(emp.id)
                else:
                    db.add_all(employees)
                    db.commit()
                    batch_processed_ids.update({emp.id for emp in employees})
                logger.info(f"Procesados {len(employees)} empleados")
            except Exception as e:
                db.rollback()
                logger.error(f"Error en batch: {e}")
                
                # Intentar uno por uno
                for emp in employees:
                    try:
                        if update_existing:
                            db.merge(emp)
                        else:
                            db.add(emp)
                        db.commit()
                        batch_processed_ids.add(emp.id)
                    except Exception as e:
                        db.rollback()
                        errors.append(f"Error with ID {emp.id}: {str(e)}")

        return batch_processed_ids

    async def process_upload(
        self, 
        file: UploadFile, 
        update_existing: bool,
        db: Session
    ) -> Dict[str, Any]:
        try:
            await validate_file_size(file)
            await validate_csv_format(file)

            processed_ids = set()
            errors = []
            
            # Leer CSV
            df = pd.read_csv(
                file.file, 
                header=None,  # Sin headers
                names=self.columns,
                na_values=['', 'NULL', 'null', 'NaN', 'nan'],
                keep_default_na=True,
                dtype={
                    'id': 'Int64',
                    'name': str,
                    'department_id': 'Int64',
                    'job_id': 'Int64'
                }
            )
            
            # Limpiar strings
            df['name'] = df['name'].str.strip()
            
            # Validar IDs
            valid_mask = df['id'].notna()
            invalid_records = df[~valid_mask]
            valid_records = df[valid_mask].copy()
            
            if len(valid_records) == 0:
                return {
                    "message": "No valid records to process",
                    "summary": {
                        "total_rows": len(df),
                        "valid_records": 0,
                        "invalid_records": len(invalid_records),
                        "reason": "No records with valid ID found"
                    }
                }
            
            # Convertir datos
            valid_records['id'] = valid_records['id'].astype(int)
            valid_records['datetime'] = pd.to_datetime(
                valid_records['datetime'],
                format='%Y-%m-%dT%H:%M:%SZ',
                errors='coerce'
            )

            logger.info(f"Procesando {len(valid_records)} registros válidos")
            
            # Procesar por lotes
            for i in range(0, len(valid_records), self.BATCH_SIZE):
                batch_df = valid_records.iloc[i:i + self.BATCH_SIZE]
                batch_processed = await self.process_batch(
                    batch_df, 
                    db, 
                    processed_ids, 
                    errors,
                    update_existing
                )
                processed_ids.update(batch_processed)
            
            # Estadísticas de nulos
            null_stats = {
                'null_names': len(valid_records[valid_records['name'].isna()]),
                'null_datetimes': len(valid_records[valid_records['datetime'].isna()]),
                'null_departments': len(valid_records[valid_records['department_id'].isna()]),
                'null_jobs': len(valid_records[valid_records['job_id'].isna()])
            }

            return {
                "message": f"Processed {len(df)} rows: {len(processed_ids)} successful, {len(invalid_records)} invalid",
                "summary": {
                    "total_rows": len(df),
                    "processed_successfully": len(processed_ids),
                    "rows_with_null_values": null_stats,
                    "invalid_records": len(invalid_records),
                    "errors": errors[:5] if errors else []
                }
            }
            
        except Exception as e:
            logger.error(f"Error en el proceso: {e}")
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail={"error": str(e), "tip": "Check if the CSV format is correct and all IDs are valid"}
            )