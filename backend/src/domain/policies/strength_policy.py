from enum import Enum, auto
from typing import Tuple


class StrengthLevel(Enum):
    VERY_WEAK = auto()
    WEAK = auto()
    FAIR = auto()
    STRONG = auto()
    PARANOID = auto()


class StrengthPolicy:
    """Evaluate password strength based on entropy bits"""
    
    # Entropy thresholds (in bits)
    THRESHOLDS = {
        StrengthLevel.VERY_WEAK: 28,
        StrengthLevel.WEAK: 36,
        StrengthLevel.FAIR: 60,
        StrengthLevel.STRONG: 128,
        StrengthLevel.PARANOID: float("inf")
    }
    
    # Labels and colors for each level
    LEVEL_INFO = {
        StrengthLevel.VERY_WEAK: ("Очень слабый", "#ff4444"),
        StrengthLevel.WEAK: ("Слабый", "#ff8844"),
        StrengthLevel.FAIR: ("Средний", "#ffdd44"),
        StrengthLevel.STRONG: ("Сильный", "#44ff44"),
        StrengthLevel.PARANOID: ("Параноидальный", "#00ccff"),
    }
    
    @classmethod
    def evaluate(cls, entropy_bits: float) -> Tuple[StrengthLevel, str, str]:
        """
        Evaluate strength level from entropy.
        Returns: (StrengthLevel, label, color)
        """
        for level, threshold in cls.THRESHOLDS.items():
            if entropy_bits < threshold:
                label, color = cls.LEVEL_INFO[level]
                return level, label, color
        
        # Fallback (should never reach here)
        label, color = cls.LEVEL_INFO[StrengthLevel.PARANOID]
        return StrengthLevel.PARANOID, label, color