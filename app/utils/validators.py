from fastapi import HTTPException, UploadFile
from typing import Set
import pandas as pd

async def validate_file_size(file: UploadFile, max_size: int = 10 * 1024 * 1024):
    """Validar tamaño del archivo"""
    size = 0
    content = await file.read(max_size + 1)
    size = len(content)
    await file.seek(0)
    
    if size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed ({max_size/1024/1024}MB)"
        )  # Este era el paréntesis que faltaba

async def validate_csv_format(file: UploadFile):
    """Validar formato básico del CSV"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="File must be a CSV"
        )

async def validate_required_columns(df: pd.DataFrame, required_columns: Set[str]):
    """Validar columnas requeridas en DataFrame"""
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_columns)}"
        )