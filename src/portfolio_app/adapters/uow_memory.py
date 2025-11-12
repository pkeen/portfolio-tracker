from portfolio_app.ports.uow import UnitOfWork
from portfolio_app.adapters.repos_memory import MemoryPortfolioRepo

# class MemoryUoW(UnitOfWork):
#     def __init__(self):
#         self.portfolios = MemoryPortfolioRepo()
#         self.outbox = []
#         self.committed = False

#     def __enter__(self): return self
#     def __exit__(self, exc_type, *_):
#         if exc_type: self.rollback()

#     def commit(self):
#         # sweep domain events from all aggregates into outbox
#         for p in self.portfolios.store.values():
#             if getattr(p, "events", None):
#                 self.outbox.extend(p.events)
#                 p.events.clear()
#         self.committed = True

#     def rollback(self):
#         self.committed = False


class MemoryUoW(UnitOfWork):
    def __init__(self):
        self.portfolios = MemoryPortfolioRepo()
        self.outbox = []
        self.committed = False

    def __enter__(self):
        print("[UoW] BEGIN")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("[UoW] ROLLBACK (exception)")
        else:
            print("[UoW] END")
        # don’t swallow exceptions; let them propagate

    def commit(self):
        # sweep domain events from all tracked aggregates into outbox
        for p in self.portfolios.store.values():
            if getattr(p, "events", None):
                self.outbox.extend(p.events)
                p.events.clear()
        self.committed = True
        print(f"[UoW] COMMIT (events -> outbox: {len(self.outbox)})")

    def rollback(self):
        self.committed = False
        print("[UoW] rollback() called")