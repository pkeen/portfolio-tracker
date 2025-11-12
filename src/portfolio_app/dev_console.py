# # Launch with: PYTHONPATH=. python -m portfolio_app.dev_console
# from datetime import date
# from decimal import Decimal

# from IPython import embed

# from portfolio_app.adapters.ouw_memory import MemoryUoW
# from portfolio_app.adapters.repos_memory import MemoryPortfolioRepo
# from portfolio_app.domain.ids import PortfolioId, SecurityId
# from portfolio_app.domain.money import Currency, Money, q
# from portfolio_app.domain.portfolio import Portfolio
# from portfolio_app.domain.transactions import CashMovement, Trade


# class FakePricing:
#     def __init__(self, table): self.table = table
#     def price(self, sec, asof, ccy): return Money(self.table[(sec.value, asof)], ccy)

# def make_portfolio(pid="P1", ccy="USD", cash=1000):
#     return Portfolio(PortfolioId(pid), Currency(ccy), Money(cash, Currency(ccy)))

# def deposit(p: Portfolio, amt, ccy="USD", d=None):
#     d = d or date.today()
#     p.record_cash(CashMovement(d, Money(q(amt), Currency(ccy))))
#     return p

# def buy(p: Portfolio, sym, qty, px, ccy="USD", d=None):
#     d = d or date.today()
#     p.record_trade(Trade(d, SecurityId(sym), q(qty), Money(q(px), Currency(ccy))))
#     return p

# def sell(p: Portfolio, sym, qty, px, ccy="USD", d=None):
#     d = d or date.today()
#     p.record_trade(Trade(d, SecurityId(sym), -q(qty), Money(q(px), Currency(ccy))))
#     return p

# def value(p: Portfolio, d, pricing):
#     return p.value(d, pricing)

# # if __name__ == "__main__":
# #     repo = MemoryPortfolioRepo()
# #     p = make_portfolio()  # preloaded portfolio
# #     repo.add(p)
# #     pricing = FakePricing({("AAPL", date(2025, 1, 2)): Decimal("60")})
# #     banner = """
# # Preloaded names:
# #   p           -> Portfolio('P1', USD, $1000)
# #   pricing     -> FakePricing table with ('AAPL', 2025-01-02) = 60
# # Helpers:
# #   deposit(p, 500)
# #   buy(p, "AAPL", 2, 100, d=date(2025,1,1))
# #   sell(p, "AAPL", 1, 110, d=date(2025,1,2))
# #   value(p, date(2025,1,2), pricing)

# # Examples:
# #   >>> buy(p, "AAPL", 2, 100, d=date(2025,1,1))
# #   >>> value(p, date(2025,1,2), pricing)
# # """
# #     embed(header=banner)


# def main(): 
#     repo = MemoryPortfolioRepo()
#     p = make_portfolio()  # preloaded portfolio
#     repo.add(p)
#     uow = MemoryUoW()
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


from datetime import date
from decimal import Decimal

try:
    from IPython import embed as _embed
    def embed(header=""): _embed(header=header)
except ImportError:
    from code import interact
    def embed(header=""): interact(banner=header, local=globals())

# --- Domain imports ---
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.ids import PortfolioId, SecurityId
from portfolio_app.domain.money import Money, Currency, q
from portfolio_app.domain.transactions import Trade, CashMovement
from portfolio_app.domain.events import TradeRecorded, CashRecorded, PositionClosed

# --- Adapters ---
from portfolio_app.adapters.uow_memory import MemoryUoW

# --- Helpers ---
class FakePricing:
    def __init__(self, table): self.table = table
    def price(self, sec, asof, ccy): return Money(self.table[(sec.value, asof)], ccy)

class FakeClock:
    def today(self): return date.today()
    def now(self):
        import datetime
        return datetime.datetime.now(datetime.timezone.utc)

# --- Globals created when main() runs ---
uow: MemoryUoW | None = None
clock: FakeClock | None = None
pricing: FakePricing | None = None

def create_portfolio(pid="P1", ccy="USD", cash=0):
    """Create and register a portfolio inside the UoW (via its repo)."""
    with uow:
        p = Portfolio(PortfolioId(pid), Currency(ccy), Money(q(cash), Currency(ccy)))
        uow.portfolios.add(p)
        uow.commit()
    print(f"Created portfolio {pid} {ccy} with cash {cash}")
    return p

def get(pid="P1"):
    return uow.portfolios.get(PortfolioId(pid))

def deposit(pid="P1", amt=0, ccy="USD", d=None):
    d = d or clock.today()
    with uow:
        p = get(pid)
        p.record_cash(CashMovement(d, Money(q(amt), Currency(ccy))), recorded_ts=clock.now())
        uow.portfolios.save(p)
        uow.commit()
    _print_last_events()

def withdraw(pid="P1", amt=0, ccy="USD", d=None):
    return deposit(pid, -amt, ccy, d)

def buy(pid="P1", sym="AAPL", qty=1, px=100, ccy="USD", d=None):
    d = d or clock.today()
    with uow:
        p = get(pid)
        t = Trade(d, SecurityId(sym), q(qty), Money(q(px), Currency(ccy)))
        p.record_trade(t, recorded_ts=clock.now())
        uow.portfolios.save(p)
        uow.commit()
    _print_last_events()

def sell(pid="P1", sym="AAPL", qty=1, px=100, ccy="USD", d=None):
    d = d or clock.today()
    with uow:
        p = get(pid)
        t = Trade(d, SecurityId(sym), -q(qty), Money(q(px), Currency(ccy)))
        p.record_trade(t, recorded_ts=clock.now())
        uow.portfolios.save(p)
        uow.commit()
    _print_last_events()

def portfolio_value(pid="P1", d=None):
    d = d or clock.today()
    p = get(pid)
    return p.value(d, pricing)

def positions(pid="P1"):
    p = get(pid)
    for pos in p.open_positions:
        print(f"{pos.security.value}: qty={pos.quantity} avg_cost={pos.avg_cost_per_share.amount}")

def cash(pid="P1"):
    p = get(pid)
    print(f"Cash: {p.cash.amount} {p.cash.currency}")

def outbox():
    return list(uow.outbox)

def clear_outbox():
    uow.outbox.clear()
    print("[UoW] outbox cleared")

def _print_last_events(n=5):
    if not uow.outbox:
        print("(no events)")
        return
    print("Last events:")
    for e in uow.outbox[-n:]:
        if isinstance(e, TradeRecorded):
            print(f"  TradeRecorded {e.side} {e.security.value} qty={e.qty} at {e.price.amount} on {e.asof}")
        elif isinstance(e, CashRecorded):
            sign = "+" if e.amount.amount >= 0 else ""
            print(f"  CashRecorded {sign}{e.amount.amount} {e.amount.currency} on {e.asof}")
        elif isinstance(e, PositionClosed):
            print(f"  PositionClosed {e.security.value} on {e.asof}")
        else:
            print(f"  {e}")

# --- Entry point ---
def main():
    """Launch interactive development console."""
    global uow, clock, pricing
    uow = MemoryUoW()
    clock = FakeClock()
    pricing = FakePricing({("AAPL", date(2025, 1, 2)): Decimal("60")})
    create_portfolio("P1", "USD", 1000)

    banner = """
Dev console ready.

Globals:
  uow       -> MemoryUoW (prints BEGIN/COMMIT/END)
  clock     -> FakeClock
  pricing   -> FakePricing with ('AAPL', 2025-01-02) = 60

Main helpers:
  create_portfolio(pid="P1", ccy="USD", cash=1000)
  deposit(pid="P1", amt=500)
  withdraw(pid="P1", amt=200)
  buy(pid="P1", sym="AAPL", qty=2, px=100)
  sell(pid="P1", sym="AAPL", qty=1, px=110)
  positions("P1"); cash("P1"); portfolio_value("P1")
  outbox(); clear_outbox()

Examples:
  >>> deposit("P1", 250)
  >>> buy("P1", "AAPL", 2, 100)
  >>> positions("P1"); cash("P1")
  >>> portfolio_value("P1", d=date(2025,1,2))
  >>> outbox()
"""
    embed(header=banner)

if __name__ == "__main__":
    main()
