# ports/repos.py
from abc import ABC, abstractmethod
from typing import Protocol
from ..domain.portfolio import Portfolio
from ..domain.ids import PortfolioId

class PortfolioRepository(ABC):
    @abstractmethod
    def get(self, pid: PortfolioId) -> Portfolio: ...
    @abstractmethod
    def add(self, portfolio: Portfolio) -> None: ...
    @abstractmethod
    def save(self, portfolio: Portfolio) -> None: ...

