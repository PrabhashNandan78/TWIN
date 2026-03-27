from dataclasses import dataclass

@dataclass
class GlobalTime:
    day: int = 0

    def advance(self, days: int = 1):
        self.day += days

