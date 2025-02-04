from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class HiredEmployee(Base):
    """Modelo para empleados contratados"""
    __tablename__ = "hired_employees"
    
    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True, index=True)
    datetime = Column(
        DateTime, 
        nullable=True, 
        default=datetime.utcnow,
        index=True
    )
    department_id = Column(
        Integer, 
        ForeignKey("departments.id"), 
        nullable=True
    )
    job_id = Column(
        Integer, 
        ForeignKey("jobs.id"), 
        nullable=True
    )
    
    # Relaciones
    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
    
    # Índices compuestos
    __table_args__ = (
        Index('ix_hired_employees_dept_job', 'department_id', 'job_id'),
        Index('ix_hired_employees_datetime_dept', 'datetime', 'department_id'),
    )

class Department(Base):
    """Modelo para departamentos"""
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=True, index=True, unique=True)
    
    # Relaciones
    employees = relationship(
        "HiredEmployee", 
        back_populates="department",
        cascade="all, delete-orphan"
    )

class Job(Base):
    """Modelo para puestos de trabajo"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=True, index=True, unique=True)
    
    # Relaciones
    employees = relationship(
        "HiredEmployee", 
        back_populates="job",
        cascade="all, delete-orphan"
    )