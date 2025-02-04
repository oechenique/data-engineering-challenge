from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class EmployeeBase(BaseModel):
    """Esquema base para empleados"""
    name: Optional[str] = None
    datetime: Optional[datetime] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None
    
    @validator('department_id', 'job_id')
    def validate_ids(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID must be positive")
        return v
    
    @validator('datetime')
    def validate_datetime(cls, v):
        if v is not None and v > datetime.now():
            raise ValueError("Datetime cannot be in the future")
        return v

class EmployeeCreate(EmployeeBase):
    """Esquema para crear empleados"""
    id: int = Field(..., gt=0)

class EmployeeInDB(EmployeeBase):
    """Esquema para empleados en DB"""
    id: int
    
    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    """Esquema base para departamentos"""
    department: str

class DepartmentCreate(DepartmentBase):
    """Esquema para crear departamentos"""
    id: int = Field(..., gt=0)

class DepartmentInDB(DepartmentBase):
    """Esquema para departamentos en DB"""
    id: int
    
    class Config:
        orm_mode = True

class JobBase(BaseModel):
    """Esquema base para trabajos"""
    job: str

class JobCreate(JobBase):
    """Esquema para crear trabajos"""
    id: int = Field(..., gt=0)

class JobInDB(JobBase):
    """Esquema para trabajos en DB"""
    id: int
    
    class Config:
        orm_mode = True

# Esquemas para métricas
class QuarterlyHiring(BaseModel):
    """Esquema para contrataciones trimestrales"""
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int

class DepartmentHiring(BaseModel):
    """Esquema para contrataciones por departamento"""
    id: int
    department: str
    hired: int