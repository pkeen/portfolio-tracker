# domain/money.py
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import NewType, Any

Currency = NewType("Currency", str)

def q(x: Any) -> Decimal:
    return Decimal(str(x))

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency = Currency("USD")

    def __post_init__(self):
        # normalize amount
        try:
            amt = Decimal(self.amount)
        except (InvalidOperation, TypeError):
            raise ValueError("Money.amount must be a valid Decimal-compatible value")
        # quantize to 2 decimals (adjust as needed)
        amt = amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", amt)

    
    def __add__(self, other: "Money") -> "Money":
        _same(self.currency, other.currency)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        _same(self.currency, other.currency)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: Decimal | int | float) -> "Money":
        return Money((self.amount * q(factor)), self.currency)

def _same(a: Currency, b: Currency):
    if a != b:
        raise ValueError(f"Currency mismatch: {a} vs {b}")
