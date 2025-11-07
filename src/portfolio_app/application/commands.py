# application/commands.py
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from ..domain.ids import PortfolioId, SecurityId
from ..domain.money import Money, Currency

@dataclass(frozen=True)
class CreatePortfolio:
    portfolio_id: str
    currency: str = "USD"

@dataclass(frozen=True)
class DepositCash:
    portfolio_id: str
    amount: float
    currency: str = "USD"
    asof: date | None = None

@dataclass(frozen=True)
class BuyShares:
    portfolio_id: str
    symbol: str
    quantity: float
    price: float
    currency: str = "USD"
    asof: date | None = None

@dataclass(frozen=True)
class SellShares(BuyShares):
    pass
