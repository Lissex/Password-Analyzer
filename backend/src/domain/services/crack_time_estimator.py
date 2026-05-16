from dataclasses import dataclass
from typing import List

from ..value_objects.entropy import Entropy
from ..value_objects.crack_time import CrackTime


@dataclass(frozen=True)
class CrackEstimate:
    scenario: str
    crack_time: CrackTime


class CrackTimeEstimator:
    """Estimate password crack time for different attack scenarios"""
    
    # Guesses per second for each scenario
    SCENARIOS = {
        "online_throttled": 100,          # 100 guesses/sec (rate limited)
        "online_unthrottled": 10_000,     # 10k guesses/sec (no rate limit)
        "offline_slow": 1_000_000,        # 1M guesses/sec (bcrypt/scrypt)
        "offline_fast": 1_000_000_000_000  # 1T guesses/sec (MD5 on GPU)
    }
    
    @classmethod
    def estimate_all(cls, entropy: Entropy) -> List[CrackEstimate]:
        """Estimate crack time for all attack scenarios"""
        estimates = []
        
        for scenario, guesses_per_second in cls.SCENARIOS.items():
            # Number of combinations = 2^entropy
            combinations = 2 ** entropy.bits
            
            # Time in seconds = combinations / guesses_per_second
            seconds = combinations / guesses_per_second
            
            estimates.append(
                CrackEstimate(
                    scenario=scenario,
                    crack_time=CrackTime(seconds=seconds)
                )
            )
        
        return estimates