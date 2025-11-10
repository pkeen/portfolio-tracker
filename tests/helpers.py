# tests/helpers.py
from datetime import date, datetime, timezone

from portfolio_app.ports.clock import Clock


class FakeClock(Clock):
    def __init__(self, d=None, dt=None):
        self._d = d or date(2025,1,1)
        self._dt = dt or datetime(2025,1,1,tzinfo=timezone.utc)
    def today(self): return self._d
    def now(self): return self._dt
