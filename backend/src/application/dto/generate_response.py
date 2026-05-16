from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import List, Dict, Any

@dataclass(frozen=True)
class GenerateResponse:
    """Response DTO for password generation"""
    password: str
    analysis_id: UUID
    analyzed_at: datetime
    entropy_bits: float
    pool_size: int
    pool_details: Dict[str, bool]
    strength_label: str
    strength_color: str
    crack_estimates: List[Dict[str, Any]]