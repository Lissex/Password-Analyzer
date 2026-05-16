from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from uuid import UUID


class AnalyzeRequestSchema(BaseModel):
    """Pydantic schema for analyze request"""
    password: str = Field(..., min_length=1, max_length=512, description="Password to analyze")


class GenerateRequestSchema(BaseModel):
    """Pydantic schema for generate request"""
    length: int = Field(16, ge=8, le=128, description="Password length")
    uppercase: bool = Field(True, description="Include uppercase letters")
    digits: bool = Field(True, description="Include digits")
    symbols: bool = Field(False, description="Include symbols")


class CrackEstimateSchema(BaseModel):
    """Pydantic schema for crack time estimate"""
    scenario: str
    seconds: float
    human_readable: str


class AnalyzeResponseSchema(BaseModel):
    """Pydantic schema for analyze response"""
    analysis_id: UUID
    analyzed_at: datetime
    entropy_bits: float
    pool_size: int
    pool_details: Dict[str, bool]
    strength_label: str
    strength_color: str
    crack_estimates: List[CrackEstimateSchema]


class GenerateResponseSchema(BaseModel):
    """Pydantic schema for generate response"""
    password: str
    analysis_id: UUID
    analyzed_at: datetime
    entropy_bits: float
    pool_size: int
    pool_details: Dict[str, bool]
    strength_label: str
    strength_color: str
    crack_estimates: List[CrackEstimateSchema]


class HistoryItemSchema(BaseModel):
    """Pydantic schema for history item"""
    id: UUID
    analyzed_at: datetime
    entropy_bits: float
    pool_size: int
    strength_label: str
    strength_color: str


class HistoryResponseSchema(BaseModel):
    """Pydantic schema for history response"""
    items: List[HistoryItemSchema]
    total: int