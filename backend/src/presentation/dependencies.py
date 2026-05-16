from typing import AsyncGenerator
from fastapi import Depends

from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.postgres_analysis_repository import PostgresAnalysisRepository
from src.domain.repositories.i_analysis_repository import IAnalysisRepository
from src.domain.services.crack_time_estimator import CrackTimeEstimator
from src.domain.policies.strength_policy import StrengthPolicy
from src.application.use_cases.analyze_password import AnalyzePasswordUseCase
from src.application.use_cases.generate_password import GeneratePasswordUseCase
from sqlalchemy.ext.asyncio import AsyncSession


# Re-export get_db from infrastructure
__all__ = ["get_db"]


async def get_analysis_repository(
    db: AsyncSession = Depends(get_db)
) -> IAnalysisRepository:
    """Get analysis repository instance"""
    return PostgresAnalysisRepository(db)


async def get_analyze_use_case(
    repo: IAnalysisRepository = Depends(get_analysis_repository)
) -> AnalyzePasswordUseCase:
    """Get analyze password use case instance"""
    return AnalyzePasswordUseCase(
        estimator=CrackTimeEstimator(),
        policy=StrengthPolicy(),
        repo=repo,
    )


async def get_generate_use_case(
    repo: IAnalysisRepository = Depends(get_analysis_repository)
) -> GeneratePasswordUseCase:
    """Get generate password use case instance"""
    return GeneratePasswordUseCase(
        estimator=CrackTimeEstimator(),
        policy=StrengthPolicy(),
        repo=repo,
    )