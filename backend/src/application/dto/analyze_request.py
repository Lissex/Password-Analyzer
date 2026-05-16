from dataclasses import dataclass

@dataclass(frozen=True)
class AnalyzeRequest:
    """Request DTO for password analysis"""
    raw_password: str