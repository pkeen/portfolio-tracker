# ports/clock.py
from abc import ABC, abstractmethod
from datetime import date, datetime, timezone


class Clock(ABC):
    @abstractmethod
    def today(self) -> date: ...
    @abstractmethod
    def now(self) -> datetime: ...

class SystemClock(Clock):
    def today(self) -> date:
        return datetime.now(timezone.utc).date()
    def now(self) -> datetime:
        return datetime.now(timezone.utc)
