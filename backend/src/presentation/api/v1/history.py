from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any

from src.domain.repositories.i_analysis_repository import IAnalysisRepository
from src.presentation.schemas.password_schemas import (
    HistoryResponseSchema,
    HistoryItemSchema,
)
from src.presentation.dependencies import get_analysis_repository

router = APIRouter(prefix="/history", tags=["history"])


@router.get(
    "",
    response_model=HistoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get recent password analyses",
    description="Returns a list of recently analyzed passwords (excluding the passwords themselves)"
)
async def get_history(
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    repo: IAnalysisRepository = Depends(get_analysis_repository),
) -> Dict[str, Any]:
    """Get recent password analyses history"""
    try:
        analyses = await repo.get_recent(limit)
        
        items = [
            HistoryItemSchema(
                id=analysis.id,
                analyzed_at=analysis.analyzed_at,
                entropy_bits=analysis.entropy.bits,
                pool_size=analysis.pool.size,
                strength_label=analysis.strength_label,
                strength_color=analysis.strength_color,
            )
            for analysis in analyses
        ]
        
        return {
            "items": [item.model_dump() for item in items],
            "total": len(items),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )