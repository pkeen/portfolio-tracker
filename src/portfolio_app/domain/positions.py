# domain/positions.py
from dataclasses import dataclass
from decimal import Decimal

from .ids import SecurityId
from .money import Money, q


@dataclass(frozen=True)
class Position:
    security: SecurityId
    quantity: Decimal
    cost_basis: Money  # total cost (FIFO/avg later; start with simple avg)

    def apply_trade(self, price: Money, qty_delta: Decimal, fees: Money | None = None) -> "Position":
        if qty_delta == 0:
            return self
        if self.quantity + qty_delta < 0:
            raise ValueError("Cannot sell more than held")

        fees = fees or Money(0, price.currency)

        # BUY
        if qty_delta > 0:
            new_qty = self.quantity + qty_delta
            added_cost = Money(price.amount * qty_delta, price.currency)
            new_cost = self.cost_basis + added_cost + fees  # include fees in basis (optional, but common)
            return Position(self.security, new_qty, new_cost)
            
        # SELL (qty_delta < 0) — reduce cost basis proportionally, avg cost stays the same
        old_qty = self.quantity
        new_qty = self.quantity + qty_delta  # qty_delta is negative
        if new_qty == 0:
            return Position(self.security, Decimal(0), Money(0, self.cost_basis.currency))

        ratio = new_qty / old_qty
        new_cost = Money(self.cost_basis.amount * ratio, self.cost_basis.currency)
        return Position(self.security, new_qty, new_cost)

    def market_value(self, px: Money) -> Money:
        return Money(px.amount * q(self.quantity), px.currency)

    @property
    def avg_cost_per_share(self) -> Money:
        if self.quantity == 0:
            return Money(0, self.cost_basis.currency)
        return Money(self.cost_basis.amount / q(self.quantity), self.cost_basis.currency)
