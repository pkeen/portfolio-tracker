from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


# Emitted whenever a buy/sell is recorded against a portfolio.
@dataclass(frozen=True)
class TradeRecorded:
    portfolio_id: PortfolioId
    asof: date
    security: SecurityId
    side: Side            # BUY/SELL
    qty: Decimal
    price: Money
    fees: Money
    ts: datetime       


# Emitted when a position size becomes zero after a sell.
@dataclass(frozen=True)
class PositionClosed:
    portfolio_id: UUID
    security: SecurityId
    ts: datetime


@dataclass(frozen=True)
class CashRecorded:
    portfolio_id: PortfolioId
    asof: date
    amount: Money       # + deposit, – withdrawal
    ts: datetime
