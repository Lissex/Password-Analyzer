from datetime import datetime, timezone
from uuid import uuid4

from src.domain.value_objects.entropy import Entropy
from src.domain.value_objects.character_pool import CharacterPool
from src.domain.services.crack_time_estimator import CrackTimeEstimator
from src.domain.policies.strength_policy import StrengthPolicy
from src.domain.repositories.i_analysis_repository import IAnalysisRepository
from src.domain.entities.password_analysis import PasswordAnalysis
from src.application.dto.analyze_response import AnalyzeResponse


class AnalyzePasswordUseCase:
    """Use case for analyzing a password"""
    
    def __init__(
        self,
        estimator: CrackTimeEstimator,
        policy: StrengthPolicy,
        repo: IAnalysisRepository,
    ):
        self._estimator = estimator
        self._policy = policy
        self._repo = repo
    
    async def execute(self, raw_password: str) -> AnalyzeResponse:
        """Execute password analysis"""
        if not raw_password:
            raise ValueError("Password cannot be empty")
        
        # 1. Build CharacterPool from password
        pool = CharacterPool.from_password(raw_password)
        
        # 2. Calculate Entropy
        entropy = Entropy.calculate(len(raw_password), pool.size)
        
        # 3. Get strength via policy
        level, strength_label, strength_color = self._policy.evaluate(entropy.bits)
        
        # 4. Estimate crack times
        crack_estimates_raw = self._estimator.estimate_all(entropy)
        crack_estimates = [
            {
                "scenario": estimate.scenario,
                "seconds": estimate.crack_time.seconds,
                "human_readable": estimate.crack_time.human_readable,
            }
            for estimate in crack_estimates_raw
        ]
        
        # 5. Build PasswordAnalysis entity
        analysis = PasswordAnalysis.create(
            entropy=entropy,
            pool=pool,
            strength_label=strength_label,
            strength_color=strength_color,
        )
        
        # 6. Save to repository
        await self._repo.save(analysis)
        
        # 7. Return AnalyzeResponse DTO
        return AnalyzeResponse(
            analysis_id=analysis.id,
            analyzed_at=analysis.analyzed_at,
            entropy_bits=entropy.bits,
            pool_size=pool.size,
            pool_details={
                "has_lowercase": pool.has_lowercase,
                "has_uppercase": pool.has_uppercase,
                "has_digits": pool.has_digits,
                "has_symbols": pool.has_symbols,
            },
            strength_label=strength_label,
            strength_color=strength_color,
            crack_estimates=crack_estimates,
        )