# application/handlers.py
from datetime import date
from decimal import Decimal
from ..ports.uow import UnitOfWork
from ..ports.pricing import PricingPort
from ..ports.clock import Clock
from ..domain.portfolio import Portfolio
from ..domain.ids import PortfolioId, SecurityId
from ..domain.money import Money, Currency, q
from ..domain.transactions import CashMovement, Trade

def handle_create_portfolio(cmd, repo):
    p = Portfolio(PortfolioId(cmd.portfolio_id), Currency(cmd.currency), Money(0, Currency(cmd.currency)))
    repo.add(p)

def handle_deposit_cash(cmd, repo, today: date):
    p = repo.get(PortfolioId(cmd.portfolio_id))
    p.record_cash(CashMovement(cmd.asof or today, Money(q(cmd.amount), Currency(cmd.currency))))
    repo.save(p)

def handle_buy_shares(cmd, repo, today: date):
    p = repo.get(PortfolioId(cmd.portfolio_id))
    t = Trade(
        asof=cmd.asof or today,
        security=SecurityId(cmd.symbol),
        quantity=q(cmd.quantity),
        price=Money(q(cmd.price), Currency(cmd.currency)),
    )
    p.record_trade(t)
    repo.save(p)

def handle_sell_shares(cmd, repo, today: date):
    p = repo.get(PortfolioId(cmd.portfolio_id))
    t = Trade(
        asof=cmd.asof or today,
        security=SecurityId(cmd.symbol),
        quantity=-q(cmd.quantity),
        price=Money(q(cmd.price), Currency(cmd.currency)),
    )
    p.record_trade(t)
    repo.save(p)
    

# def handle_create_portfolio(cmd, uow: UnitOfWork):
#     with uow:
#         p = Portfolio(PortfolioId(cmd.portfolio_id), Currency(cmd.currency), Money(0, Currency(cmd.currency)))
#         uow.portfolios.add(p)
#         uow.commit()

# def handle_deposit_cash(cmd, uow: UnitOfWork, clock: Clock):
#     with uow:
#         p = uow.portfolios.get(PortfolioId(cmd.portfolio_id))
#         asof = cmd.asof or clock.today()
#         p.record_cash(CashMovement(asof, Money(q(cmd.amount), Currency(cmd.currency))))
#         uow.portfolios.save(p)
#         uow.commit()

# def handle_buy_shares(cmd, uow: UnitOfWork, clock: Clock):
#     with uow:
#         p = uow.portfolios.get(PortfolioId(cmd.portfolio_id))
#         asof = cmd.asof or clock.today()
#         t = Trade(
#             asof=asof,
#             security=SecurityId(cmd.symbol),
#             quantity=q(cmd.quantity),
#             price=Money(q(cmd.price), Currency(cmd.currency)),
#             fees=Money(0, Currency(cmd.currency)),
#         )
#         p.record_trade(t)
#         uow.portfolios.save(p)
#         uow.commit()

# def handle_sell_shares(cmd, uow: UnitOfWork, clock: Clock):
#     with uow:
#         p = uow.portfolios.get(PortfolioId(cmd.portfolio_id))
#         asof = cmd.asof or clock.today()
#         t = Trade(
#             asof=asof,
#             security=SecurityId(cmd.symbol),
#             quantity=-q(cmd.quantity),
#             price=Money(q(cmd.price), Currency(cmd.currency)),
#             fees=Money(0, Currency(cmd.currency)),
#         )
#         p.record_trade(t)
#         uow.portfolios.save(p)
#         uow.commit()
