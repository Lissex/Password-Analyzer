from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from src.application.use_cases.analyze_password import AnalyzePasswordUseCase
from src.presentation.schemas.password_schemas import (
    AnalyzeRequestSchema,
    AnalyzeResponseSchema,
)
from src.presentation.dependencies import get_analyze_use_case

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post(
    "",
    response_model=AnalyzeResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Analyze password strength",
    description="Analyzes a password and returns entropy, crack time estimates, and strength metrics"
)
async def analyze_password(
    request: AnalyzeRequestSchema,
    use_case: AnalyzePasswordUseCase = Depends(get_analyze_use_case),
) -> Dict[str, Any]:
    """Analyze password endpoint"""
    try:
        result = await use_case.execute(request.password)
        return result.__dict__
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )   