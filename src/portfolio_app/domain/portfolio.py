# domain/portfolio.py
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Dict, Iterable, List

from .events import PositionClosed, TransactionRecorded
from .ids import PortfolioId, SecurityId
from .money import Currency, Money, q
from .positions import Position
from .transactions import CashMovement, Trade


@dataclass
class Portfolio:
    id: PortfolioId
    base_ccy: Currency
    _cash: Money = field(default_factory=lambda: Money(0, Currency("USD")))
    _positions: Dict[str, Position] = field(default_factory=dict)
    events: List[object] = field(default_factory=list)

    def record_cash(self, mov: CashMovement) -> None:
        _ensure_currency(self.base_ccy, mov.amount.currency)
        self._cash = self._cash + mov.amount
        self.events.append(TransactionRecorded(self.id, mov.asof, None, "cash"))

    def record_trade(self, t: Trade) -> None:
        _ensure_currency(self.base_ccy, t.price.currency)
        # update position
        pos = self._positions.get(t.security.value, Position(t.security, Decimal(0), Money(0, self.base_ccy)))
        self._positions[t.security.value] = pos.apply_trade(t.price, t.quantity)
        # update cash
        self._cash = self._cash + t.cash_impact
        self.events.append(TransactionRecorded(self.id, t.asof, t.security, "trade", t.side, t.ts))
        # emit close event if needed
        if self._positions[t.security.value].quantity == 0:
            self.events.append(PositionClosed(self.id, t.security, t.asof))

    @property
    def cash(self) -> Money:
        return self._cash

    @property
    def open_positions(self) -> Iterable[Position]:
        return (p for p in self._positions.values() if p.quantity != 0)

    def position_of(self, sec: SecurityId) -> Position | None:
        return self._positions.get(sec.value)

    def value(self, asof: date, pricing_port) -> Money:
        """
        pricing_port: Port with .price(SecurityId, asof, ccy)->Money
        """
        total = self._cash
        for pos in self.open_positions:
            px = pricing_port.price(pos.security, asof, self.base_ccy)
            total = total + pos.market_value(px)
        return total

def _ensure_currency(a: Currency, b: Currency):
    if a != b:
        # First version keeps one-currency portfolios; add FX later.
        raise ValueError(f"Cross-currency not supported yet: {a} vs {b}")
