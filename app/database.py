from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException
import logging

from .config import get_config

logger = logging.getLogger(__name__)
config = get_config()

# Crear engine con pooling
engine = create_engine(
    config.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ 🔥 FIX: get_db() sin `@contextmanager`
def get_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))  # Verificar conexión
        yield db  # ✅ Esto lo maneja FastAPI automáticamente
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=503, detail="Database connection error")
    finally:
        db.close()

def init_db() -> None:
    """Inicializar base de datos creando tablas"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def reset_db() -> None:
    """Reset completo de la base de datos"""
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        logger.info("Database reset successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error resetting database: {str(e)}")
        raise