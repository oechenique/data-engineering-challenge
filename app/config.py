import os
from dotenv import load_dotenv
from functools import lru_cache
from typing import Optional
from urllib.parse import quote_plus
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class Config:
    """
    Configuración central de la aplicación.
    Maneja variables de entorno y configuraciones globales.
    """
    # Database settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "ToKy04g@9GaE")
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "globant_db")
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Globant Data Engineering Challenge"
    VERSION: str = "1.0.0"
    
    # Processing settings
    BATCH_SIZE: int = 1000
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    def __init__(self):
        """Validar configuración crítica al inicializar"""
        self.validate_config()
    
    def validate_config(self):
        """Validar que existan las variables críticas"""
        if not all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME]):
            msg = "Missing critical database configuration"
            logger.error(msg)
            raise ValueError(msg)

    @property
    def DATABASE_URL(self) -> str:
        """Construir URL de conexión a la base de datos"""
        try:
            encoded_password = quote_plus(self.DB_PASSWORD)
            return f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        except Exception as e:
            logger.error(f"Error building DATABASE_URL: {str(e)}")
            raise

@lru_cache()
def get_config() -> Config:
    """
    Obtener configuración con cache.
    Returns:
        Config: Instancia única de configuración
    """
    return Config()