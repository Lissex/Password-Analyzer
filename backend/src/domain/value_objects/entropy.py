from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Entropy:
    bits: float

    @classmethod
    def calculate(cls, length: int, pool_size: int) -> "Entropy":
        """Calculate entropy in bits: length * log2(pool_size)"""
        if length <= 0:
            raise ValueError("Password length must be positive")
        if pool_size <= 1:
            raise ValueError("Pool size must be greater than 1")
        
        bits = length * math.log2(pool_size)
        return cls(bits=round(bits, 2))

    def __post_init__(self):
        if self.bits < 0:
            raise ValueError("Entropy cannot be negative")