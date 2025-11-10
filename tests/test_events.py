from datetime import date
from decimal import Decimal
from portfolio_app.domain.portfolio import Portfolio
from portfolio_app.domain.ids import PortfolioId, SecurityId
from portfolio_app.domain.money import Money, Currency, q
from portfolio_app.domain.transactions import Trade, CashMovement
from portfolio_app.domain.events import TradeRecorded, CashRecorded

def test_cash_emits_event():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(0, Currency("USD")))
    p.record_cash(CashMovement(date(2025,1,1), Money(100, Currency("USD"))), recorded_ts=None)
    assert any(isinstance(e, CashRecorded) for e in p.events)

def test_trade_emits_event_and_maybe_close():
    p = Portfolio(PortfolioId("P1"), Currency("USD"), Money(1000, Currency("USD")))
    p.record_trade(Trade(date(2025,1,1), SecurityId("AAPL"), q(2), Money(100, Currency("USD"))))
    assert any(isinstance(e, TradeRecorded) for e in p.events)
