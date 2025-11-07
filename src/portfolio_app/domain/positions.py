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

    def apply_trade(self, price: Money, qty_delta: Decimal) -> "Position":
        if qty_delta == 0:
            return self
        if self.quantity + qty_delta < 0:
            raise ValueError("Cannot sell more than held")
        # simple moving average cost basis for now
        if qty_delta > 0:
            new_qty = self.quantity + qty_delta
            new_cost = Money(self.cost_basis.amount + price.amount * q(qty_delta), price.currency)
            return Position(self.security, new_qty, new_cost)
        else:
            # selling reduces quantity and cost_basis proportionally
            sell_fraction = (self.quantity + qty_delta) / self.quantity if self.quantity else q(0)
            new_qty = self.quantity + qty_delta
            new_cost = Money(self.cost_basis.amount * sell_fraction, self.cost_basis.currency)
            return Position(self.security, new_qty, new_cost)

    def market_value(self, px: Money) -> Money:
        return Money(px.amount * q(self.quantity), px.currency)

    @property
    def avg_cost_per_share(self) -> Money:
        if self.quantity == 0:
            return Money(0, self.cost_basis.currency)
        return Money(self.cost_basis.amount / q(self.quantity), self.cost_basis.currency)
