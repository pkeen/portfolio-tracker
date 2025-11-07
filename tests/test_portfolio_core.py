# tests/test_portfolio_core.py
from datetime import date
from decimal import Decimal
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.ids import PortfolioId, SecurityId
from portfolio_app.domain.money import Money, Currency, q
from portfolio_app.domain.transactions import CashMovement, Trade

class FakePricing:
    def __init__(self, table): self.table = table
    def price(self, sec, asof, ccy): return Money(self.table[(sec.value, asof)], ccy)

def test_buy_updates_position_and_cash():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(1000, Currency("USD")))
    p.record_trade(Trade(date(2025,1,1), SecurityId("AAPL"), q(2), Money(100)))
    assert p.cash.amount == Decimal("800.00")
    pos = p.position_of(SecurityId("AAPL"))
    assert pos.quantity == Decimal("2")
    assert pos.avg_cost_per_share.amount == Decimal("100.00")

def test_cannot_sell_more_than_held():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(0, Currency("USD")))
    p.record_trade(Trade(date(2025,1,1), SecurityId("AAPL"), q(1), Money(10)))
    try:
        p.record_trade(Trade(date(2025,1,2), SecurityId("AAPL"), q(-2), Money(9)))
        assert False, "Expected error"
    except ValueError:
        assert True

def test_portfolio_value_uses_pricing_port():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(200, Currency("USD")))
    p.record_trade(Trade(date(2025,1,1), SecurityId("AAPL"), q(3), Money(50)))
    pricing = FakePricing({("AAPL", date(2025,1,2)): Decimal("60")})
    v = p.value(date(2025,1,2), pricing)
    # 200 cash + 3*60=180 -> 380
    assert v.amount == Decimal("230.00")
