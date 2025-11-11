# Launch with: PYTHONPATH=. python -m portfolio_app.dev_console
from datetime import date
from decimal import Decimal

from IPython import embed

from portfolio_app.adapters.repos_memory import MemoryPortfolioRepo
from portfolio_app.domain.ids import PortfolioId, SecurityId
from portfolio_app.domain.money import Currency, Money, q
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.transactions import CashMovement, Trade


class FakePricing:
    def __init__(self, table): self.table = table
    def price(self, sec, asof, ccy): return Money(self.table[(sec.value, asof)], ccy)

def make_portfolio(pid="P1", ccy="USD", cash=1000):
    return Portfolio(PortfolioId(pid), Currency(ccy), Money(cash, Currency(ccy)))

def deposit(p: Portfolio, amt, ccy="USD", d=None):
    d = d or date.today()
    p.record_cash(CashMovement(d, Money(q(amt), Currency(ccy))))
    return p

def buy(p: Portfolio, sym, qty, px, ccy="USD", d=None):
    d = d or date.today()
    p.record_trade(Trade(d, SecurityId(sym), q(qty), Money(q(px), Currency(ccy))))
    return p

def sell(p: Portfolio, sym, qty, px, ccy="USD", d=None):
    d = d or date.today()
    p.record_trade(Trade(d, SecurityId(sym), -q(qty), Money(q(px), Currency(ccy))))
    return p

def value(p: Portfolio, d, pricing):
    return p.value(d, pricing)

# if __name__ == "__main__":
#     repo = MemoryPortfolioRepo()
#     p = make_portfolio()  # preloaded portfolio
#     repo.add(p)
#     pricing = FakePricing({("AAPL", date(2025, 1, 2)): Decimal("60")})
#     banner = """
# Preloaded names:
#   p           -> Portfolio('P1', USD, $1000)
#   pricing     -> FakePricing table with ('AAPL', 2025-01-02) = 60
# Helpers:
#   deposit(p, 500)
#   buy(p, "AAPL", 2, 100, d=date(2025,1,1))
#   sell(p, "AAPL", 1, 110, d=date(2025,1,2))
#   value(p, date(2025,1,2), pricing)

# Examples:
#   >>> buy(p, "AAPL", 2, 100, d=date(2025,1,1))
#   >>> value(p, date(2025,1,2), pricing)
# """
#     embed(header=banner)


def main(): 
    repo = MemoryPortfolioRepo()
    p = make_portfolio()  # preloaded portfolio
    repo.add(p)
    pricing = FakePricing({("AAPL", date(2025, 1, 2)): Decimal("60")})
    banner = """
Preloaded names:
  p           -> Portfolio('P1', USD, $1000)
  pricing     -> FakePricing table with ('AAPL', 2025-01-02) = 60
Helpers:
  deposit(p, 500)
  buy(p, "AAPL", 2, 100, d=date(2025,1,1))
  sell(p, "AAPL", 1, 110, d=date(2025,1,2))
  value(p, date(2025,1,2), pricing)

Examples:
  >>> buy(p, "AAPL", 2, 100, d=date(2025,1,1))
  >>> value(p, date(2025,1,2), pricing)
"""
    embed(header=banner)
