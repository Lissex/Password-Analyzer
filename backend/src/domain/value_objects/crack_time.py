from dataclasses import dataclass


@dataclass(frozen=True)
class CrackTime:
    seconds: float

    @property
    def human_readable(self) -> str:
        """Convert seconds to human readable format"""
        if self.seconds < 0:
            return "invalid"

        if self.seconds < 1:
            return "instant"

        if self.seconds < 60:
            return f"{int(self.seconds)} сек"

        minutes = self.seconds / 60
        if minutes < 60:
            return f"{int(minutes)} мин"

        hours = minutes / 60
        if hours < 24:
            return f"{int(hours)} ч"

        days = hours / 24
        if days < 365:
            return f"{int(days)} дней"

        years = days / 365
        if years < 1000:
            return f"{int(years)} лет"

        thousand_years = years / 1000
        if thousand_years < 1000:
            return f"{int(thousand_years)} тыс. лет"

        million_years = thousand_years / 1000
        return f"{int(million_years)} млн лет"

    def __post_init__(self):
        if self.seconds < 0:
            raise ValueError("Crack time cannot be negative")