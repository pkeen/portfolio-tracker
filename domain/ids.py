# domain/ids.py
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class PortfolioId:
    value: UUID

@dataclass(frozen=True)
class SecurityId:
    value: str  # e.g., "AAPL" or ISIN/CUSIP


@dataclass(frozen=True, slots=True)
class TradeId:
    value: UUID

    @classmethod
    def new(cls) -> "TradeId":
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)