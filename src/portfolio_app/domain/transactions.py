# domain/transactions.py
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum

from .ids import SecurityId
from .money import Money


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass(frozen=True)
class Trade:
    asof: date
    security: SecurityId
    quantity: Decimal  # positive for buy, negative for sell
    price: Money       # per-unit
    fees: Money = Money(0)

    @property
    def side(self) -> Side:
        if self.quantity > 0:
            return Side.BUY
        if self.quantity < 0:
            return Side.SELL
        raise ValueError("Zero-quantity trade has no side")

    @property
    def cash_impact(self) -> Money:
        # buy reduces cash, sell increases cash
        gross = self.price * self.quantity
        # quantity may be negative -> gross negative -> subtract fees accordingly
        return Money(-(gross.amount) - self.fees.amount, self.price.currency)

@dataclass(frozen=True)
class CashMovement:
    asof: date
    amount: Money  # positive deposit, negative withdrawal