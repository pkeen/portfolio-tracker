from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


# Emitted whenever a buy/sell is recorded against a portfolio.
@dataclass(frozen=True)
class TransactionRecorded:
    portfolio_id: UUID
    ticker: str          # keep simple to avoid circular deps on value objects
    qty: int
    price: Decimal
    side: str            # "BUY" | "SELL"
    ts: datetime


# Emitted when a position size becomes zero after a sell.
@dataclass(frozen=True)
class PositionClosed:
    portfolio_id: UUID
    ticker: str
    ts: datetime
