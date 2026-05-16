from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from ..value_objects.entropy import Entropy
from ..value_objects.character_pool import CharacterPool


@dataclass(frozen=True)
class PasswordAnalysis:
    id: UUID
    analyzed_at: datetime
    entropy: Entropy
    pool: CharacterPool
    strength_label: str
    strength_color: str

    @classmethod
    def create(
        cls,
        entropy: Entropy,
        pool: CharacterPool,
        strength_label: str,
        strength_color: str,
    ) -> "PasswordAnalysis":
        return cls(
            id=uuid4(),
            analyzed_at=datetime.utcnow(),
            entropy=entropy,
            pool=pool,
            strength_label=strength_label,
            strength_color=strength_color,
        )