import secrets
import string
from datetime import datetime, timezone
from uuid import uuid4

from src.domain.value_objects.entropy import Entropy
from src.domain.value_objects.character_pool import CharacterPool
from src.domain.services.crack_time_estimator import CrackTimeEstimator
from src.domain.policies.strength_policy import StrengthPolicy
from src.domain.repositories.i_analysis_repository import IAnalysisRepository
from src.domain.entities.password_analysis import PasswordAnalysis
from src.application.dto.generate_response import GenerateResponse


class GeneratePasswordUseCase:
    """Use case for generating a secure password"""
    
    def __init__(
        self,
        estimator: CrackTimeEstimator,
        policy: StrengthPolicy,
        repo: IAnalysisRepository,
    ):
        self._estimator = estimator
        self._policy = policy
        self._repo = repo
    
    async def execute(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
    ) -> GenerateResponse:
        """Generate and analyze a secure password"""
        
        # Build charset based on flags
        charset = string.ascii_lowercase
        
        if use_uppercase:
            charset += string.ascii_uppercase
        if use_digits:
            charset += string.digits
        if use_symbols:
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if len(charset) < 2:
            raise ValueError("At least one character set must be enabled")
        
        # Generate password using secrets (cryptographically secure)
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        # Run analysis pipeline
        pool = CharacterPool(
            has_lowercase=True,  # Always true because we always include lowercase
            has_uppercase=use_uppercase,
            has_digits=use_digits,
            has_symbols=use_symbols,
        )
        
        entropy = Entropy.calculate(length, pool.size)
        level, strength_label, strength_color = self._policy.evaluate(entropy.bits)
        
        crack_estimates_raw = self._estimator.estimate_all(entropy)
        crack_estimates = [
            {
                "scenario": estimate.scenario,
                "seconds": estimate.crack_time.seconds,
                "human_readable": estimate.crack_time.human_readable,
            }
            for estimate in crack_estimates_raw
        ]
        
        # Create and save entity
        analysis = PasswordAnalysis.create(
            entropy=entropy,
            pool=pool,
            strength_label=strength_label,
            strength_color=strength_color,
        )
        
        await self._repo.save(analysis)
        
        return GenerateResponse(
            password=password,
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