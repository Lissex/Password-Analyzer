from fastapi import APIRouter
from .analyze import router as analyze_router
from .generate import router as generate_router
from .history import router as history_router

router = APIRouter(prefix="/api/v1")
router.include_router(analyze_router)
router.include_router(generate_router)
router.include_router(history_router)