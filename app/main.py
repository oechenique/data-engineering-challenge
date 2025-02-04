from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import employees, departments, jobs, metrics
import logging

logger = logging.getLogger(__name__)

# Crear app
app = FastAPI(
    title="Globant Data Engineering Challenge",
    description="API for processing and analyzing hiring data",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(
    employees.router,
    prefix="/api/v1",
    tags=["employees"]
)
app.include_router(
    departments.router,
    prefix="/api/v1",
    tags=["departments"]
)
app.include_router(
    jobs.router,
    prefix="/api/v1",
    tags=["jobs"]
)
app.include_router(
    metrics.router,
    prefix="/api/v1/metrics",
    tags=["metrics"]
)

@app.on_event("startup")
async def startup_event():
    """Inicializar app en startup"""
    try:
        init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.get("/api/health")
async def health_check():
    """Endpoint para health check"""
    return {"status": "healthy"}

@app.post("/api/v1/reset-database")
async def reset_database():
    """Endpoint para reset manual de DB"""
    try:
        reset_db()
        return {"message": "Database reset successfully"}
    except Exception as e:
        logger.error(f"Reset error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))