# tests/test_portfolio_core.py
from datetime import date
from decimal import Decimal

from helpers import FakeClock

from portfolio_app.domain.events import CashRecorded
from portfolio_app.domain.ids import PortfolioId, SecurityId
from portfolio_app.domain.money import Currency, Money, q
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.positions import Position
from portfolio_app.domain.transactions import CashMovement, Trade

clock = FakeClock()

class FakePricing:
    def __init__(self, table): self.table = table
    def price(self, sec, asof, ccy): return Money(self.table[(sec.value, asof)], ccy)

def test_cash_recorded():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(1000, Currency("USD")))
    p.record_cash(CashMovement(date(2025,1,1), Money(500)), clock.now())
    assert p.cash.amount == Decimal("1500.00")
    assert any(isinstance(e, CashRecorded) for e in p.events)

def test_buy_updates_position_and_cash():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(1000, Currency("USD")))
    p.record_trade(Trade(date(2025,1,1), SecurityId("AAPL"), q(2), Money(100)), clock.now())
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



def test_weighted_average_updates_on_buys():
    pos = Position(SecurityId("AAPL"), Decimal(0), Money(0, Currency("USD")))
    pos = pos.apply_trade(Money(100, Currency("USD")), q(2))  # cost 200
    pos = pos.apply_trade(Money(110, Currency("USD")), q(3))  # cost +330 = 530, qty 5
    assert pos.quantity == Decimal("5")
    assert pos.avg_cost_per_share.amount == Decimal("106.00")  # 530/5 = 106.00



def test_weighted_average_updates_on_buys():
    pos = Position(SecurityId("AAPL"), Decimal(0), Money(0, Currency("USD")))
    pos = pos.apply_trade(Money(100, Currency("USD")), q(2))  # cost 200
    pos = pos.apply_trade(Money(110, Currency("USD")), q(3))  # cost +330 = 530, qty 5
    assert pos.quantity == Decimal("5")
    assert pos.avg_cost_per_share.amount == Decimal("106.00")  # 530/5 = 106.00

def test_avg_cost_constant_on_sells_average_cost_method():
    pos = Position(SecurityId("AAPL"), Decimal(0), Money(0, Currency("USD")))
    pos = pos.apply_trade(Money(100, Currency("USD")), q(2))  # qty2 cost200 avg100
    pos = pos.apply_trade(Money(110, Currency("USD")), q(3))  # qty5 cost530 avg106
    pos2 = pos.apply_trade(Money(120, Currency("USD")), q(-2))  # sell 2, avg should stay 106
    assert pos2.quantity == Decimal("3")
    assert pos2.avg_cost_per_share.amount == Decimal("106.00")
    # cost basis should be 3 * 106 = 318
    assert pos2.cost_basis.amount == Decimal("318.00")

def test_weighted_average_includes_buy_fees_if_configured():
    pos = Position(SecurityId("AAPL"), Decimal(0), Money(0, Currency("USD")))
    pos = pos.apply_trade(Money(100, Currency("USD")), q(2), fees=Money(10, Currency("USD")))
    # total cost = 200 + 10 = 210, qty=2 => avg = 105
    assert pos.avg_cost_per_share.amount == Decimal("105.00")