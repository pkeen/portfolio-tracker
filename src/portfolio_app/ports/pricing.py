# ports/pricing.py
from abc import ABC, abstractmethod
from datetime import date
from ..domain.ids import SecurityId
from ..domain.money import Money, Currency

class PricingPort(ABC):
    @abstractmethod
    def price(self, security: SecurityId, asof: date, currency: Currency) -> Money: ...
