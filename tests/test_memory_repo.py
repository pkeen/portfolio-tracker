from portfolio_app.adapters.repos_memory import MemoryPortfolioRepo
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.ids import PortfolioId
from portfolio_app.domain.money import Money, Currency
from portfolio_app.domain.transactions import CashMovement
from datetime import date

def test_memory_repo_roundtrip():
    repo = MemoryPortfolioRepo()
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(0, Currency("USD")))
    repo.add(p)

    loaded = repo.get(PortfolioId("P1"))
    assert loaded is p  # same object in memory

    # mutate aggregate then save
    loaded.record_cash(CashMovement(date.today(), Money(100, Currency("USD"))))
    repo.save(loaded)

    again = repo.get(PortfolioId("P1"))
    assert again.cash.amount == Money(100, Currency("USD")).amount
