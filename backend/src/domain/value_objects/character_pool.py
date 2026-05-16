from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterPool:
    has_lowercase: bool
    has_uppercase: bool
    has_digits: bool
    has_symbols: bool

    @property
    def size(self) -> int:
        """Calculate total pool size based on character sets used"""
        size = 0
        if self.has_lowercase:
            size += 26  # a-z
        if self.has_uppercase:
            size += 26  # A-Z
        if self.has_digits:
            size += 10  # 0-9
        if self.has_symbols:
            size += 32  # Common symbols: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        return size

    @classmethod
    def from_password(cls, password: str) -> "CharacterPool":
        """Analyze password and determine which character sets are used"""
        return cls(
            has_lowercase=any(c.islower() for c in password),
            has_uppercase=any(c.isupper() for c in password),
            has_digits=any(c.isdigit() for c in password),
            has_symbols=any(not c.isalnum() for c in password),
        )