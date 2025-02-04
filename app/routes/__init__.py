from fastapi import APIRouter
from .employees import router as employees_router
from .departments import router as departments_router
from .jobs import router as jobs_router
from .metrics import router as metrics_router

router = APIRouter()
router.include_router(employees_router, prefix="/employees", tags=["employees"])
router.include_router(departments_router, prefix="/departments", tags=["departments"])
router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
router.include_router(metrics_router, prefix="/metrics", tags=["metrics"])