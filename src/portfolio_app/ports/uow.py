# ports/uow.py
# src/portfolio_app/ports/uow.py
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

from portfolio_app.ports.repos import PortfolioRepository

from .repos import PortfolioRepository


class UnitOfWork(ABC):
    # repositories available within the UoW
    portfolios: PortfolioRepository

    # context manager defaults (can be overridden)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        # by default do nothing; concrete UoWs decide commit/rollback policy
        return False  # don’t swallow exceptions

    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def rollback(self) -> None: ...
