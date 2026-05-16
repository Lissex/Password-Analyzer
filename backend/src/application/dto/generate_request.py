from dataclasses import dataclass

@dataclass(frozen=True)
class GenerateRequest:
    """Request DTO for password generation"""
    length: int = 16
    uppercase: bool = True
    digits: bool = True
    symbols: bool = True
    
    def __post_init__(self):
        if self.length < 4:
            raise ValueError("Password length must be at least 4")
        if self.length > 128:
            raise ValueError("Password length must be at most 128")