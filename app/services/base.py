from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType]):
    """Servicio base con operaciones comunes"""
    
    def __init__(self, model: ModelType):
        self.model = model
    
    def get(self, db: Session, id: int) -> ModelType:
        """Obtener por ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtener múltiples registros"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Crear un registro"""
        try:
            obj_in_data = obj_in.dict()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))