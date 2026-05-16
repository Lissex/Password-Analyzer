from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from src.application.use_cases.generate_password import GeneratePasswordUseCase
from src.presentation.schemas.password_schemas import (
    GenerateRequestSchema,
    GenerateResponseSchema,
)
from src.presentation.dependencies import get_generate_use_case

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post(
    "",
    response_model=GenerateResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Generate strong password",
    description="Generates a cryptographically secure password and analyzes its strength"
)
async def generate_password(
    request: GenerateRequestSchema,
    use_case: GeneratePasswordUseCase = Depends(get_generate_use_case),
) -> Dict[str, Any]:
    """Generate password endpoint"""
    try:
        result = await use_case.execute(
            length=request.length,
            use_uppercase=request.uppercase,
            use_digits=request.digits,
            use_symbols=request.symbols,
        )
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