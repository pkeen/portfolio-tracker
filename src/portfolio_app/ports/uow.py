# ports/uow.py
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from .repos import PortfolioRepository

class UnitOfWork(ABC, AbstractContextManager):
    portfolios: PortfolioRepository

    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def rollback(self) -> None: ...
