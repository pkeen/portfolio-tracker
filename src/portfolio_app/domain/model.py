from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from uuid import UUID, uuid4

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

@dataclass(frozen=True, slots=True)
class Ticker:
    symbol: str

    def __post_init__(self):
        s = self.symbol.strip().upper()
        if not s:
            raise ValueError("Ticker.symbol must be non-empty")
        object.__setattr__(self, "symbol", s)

# @dataclass(frozen=True, slots=True)
# class Money:
#     amount: Decimal
#     currency: Currency

#     def __post_init__(self):
#         # normalize amount
#         try:
#             amt = Decimal(self.amount)
#         except (InvalidOperation, TypeError):
#             raise ValueError("Money.amount must be a valid Decimal-compatible value")
#         # quantize to 2 decimals (adjust as needed)
#         amt = amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
#         object.__setattr__(self, "amount", amt)

#     def __add__(self, other: "Money") -> "Money":
#         if self.currency != other.currency:
#             raise ValueError("Cannot add Money with different currencies")
#         return Money(self.amount + other.amount, self.currency)

#     def __sub__(self, other: "Money") -> "Money":
#         if self.currency != other.currency:
#             raise ValueError("Cannot subtract Money with different currencies")
#         return Money(self.amount - other.amount, self.currency)

class TradeType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    
    def __str__(self):
        return self.value

@dataclass(frozen=True, slots=True)
class Quantity: 
    units: int

    # non-negative, add/subtract only via methods.
    def __post_init__(self):
        if self.units < 0:
            raise ValueError("Quantity.units must be non-negative")



    

@dataclass
class Position: 
    ticker: Ticker
    quantity: Quantity
    cost_basis: Money


@dataclass
class Trade:
    id: TradeId 
    ticker: Ticker
    qty: Quantity
    price: Money
    trade_type: TradeType
    ts: datetime

# @dataclass
# class Portfolio:
#     id: UUID
#     base_currency: Currency
#     positions: dict[Ticker, Position]
#     cash: Money

#     # apply_trade(trade: Trade) — updates cash, quantity, avg cost (buy/sell rules).
#     def apply_trade(self, trade: Trade):
#         pass
