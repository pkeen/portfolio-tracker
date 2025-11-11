from portfolio_app.ports.repos import PortfolioRepository
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.ids import PortfolioId

class MemoryPortfolioRepo(PortfolioRepository):
    def __init__(self):
        # pid.value -> Portfolio
        self.store: dict[str, Portfolio] = {}

    def get(self, pid: PortfolioId) -> Portfolio | None:
        return self.store.get(pid.value)

    def add(self, portfolio: Portfolio) -> None:
        self.store[portfolio.id.value] = portfolio

    def save(self, portfolio: Portfolio) -> None:
        # in memory we just overwrite the reference
        self.store[portfolio.id.value] = portfolio
