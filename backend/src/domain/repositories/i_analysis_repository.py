from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from ..entities.password_analysis import PasswordAnalysis


class IAnalysisRepository(ABC):
    """Repository interface for password analysis (lives in domain layer)"""
    
    @abstractmethod
    async def save(self, analysis: PasswordAnalysis) -> None:
        """Save a password analysis"""
        pass
    
    @abstractmethod
    async def get_recent(self, limit: int) -> List[PasswordAnalysis]:
        """Get recent analyses, ordered by analyzed_at descending"""
        pass
    
    @abstractmethod
    async def get_by_id(self, analysis_id: UUID) -> PasswordAnalysis | None:
        """Get analysis by ID"""
        pass