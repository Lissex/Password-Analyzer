from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.password_analysis import PasswordAnalysis
from src.domain.repositories.i_analysis_repository import IAnalysisRepository
from src.domain.value_objects.entropy import Entropy
from src.domain.value_objects.character_pool import CharacterPool
from src.infrastructure.database.models import PasswordAnalysisModel

class PostgresAnalysisRepository(IAnalysisRepository):
    """PostgreSQL implementation of analysis repository"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def save(self, analysis: PasswordAnalysis) -> None:
        """Save analysis to database"""
        model = PasswordAnalysisModel(
            id=analysis.id,
            analyzed_at=analysis.analyzed_at,
            entropy_bits=analysis.entropy.bits,
            pool_size=analysis.pool.size,
            has_lowercase=analysis.pool.has_lowercase,
            has_uppercase=analysis.pool.has_uppercase,
            has_digits=analysis.pool.has_digits,
            has_symbols=analysis.pool.has_symbols,
            strength_label=analysis.strength_label,
            strength_color=analysis.strength_color,
        )
        self._session.add(model)
        await self._session.commit()
    
    async def get_recent(self, limit: int) -> List[PasswordAnalysis]:
        """Get recent analyses"""
        query = (
            select(PasswordAnalysisModel)
            .order_by(PasswordAnalysisModel.analyzed_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()
        
        return [self._to_domain(model) for model in models]
    
    async def get_by_id(self, analysis_id: UUID) -> Optional[PasswordAnalysis]:
        """Get analysis by ID"""
        query = select(PasswordAnalysisModel).where(
            PasswordAnalysisModel.id == analysis_id
        )
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._to_domain(model)
    
    def _to_domain(self, model: PasswordAnalysisModel) -> PasswordAnalysis:
        """Map ORM model to domain entity"""
        pool = CharacterPool(
            has_lowercase=model.has_lowercase,
            has_uppercase=model.has_uppercase,
            has_digits=model.has_digits,
            has_symbols=model.has_symbols,
        )
        
        entropy = Entropy(bits=model.entropy_bits)
        
        return PasswordAnalysis(
            id=model.id,
            analyzed_at=model.analyzed_at,
            entropy=entropy,
            pool=pool,
            strength_label=model.strength_label,
            strength_color=model.strength_color,
        )