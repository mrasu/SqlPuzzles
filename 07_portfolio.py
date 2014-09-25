from sqlalchemy import Integer, Column, String, ForeignKey, Date, PrimaryKeyConstraint, and_, func
from sqlalchemy.orm import aliased, Query
from util import Base, session


class Portfolio(Base):
    __tablename__ = "Portfolios"

    file_id = Column(Integer, primary_key=True)
    stuff = Column(String(15))


class Succession(Base):
    __tablename__ = "succession"

    chain = Column(Integer, nullable=False)
    next = Column(Integer, nullable=False)
    file_id = Column(Integer, ForeignKey(Portfolio.file_id))
    suc_date = Column(Date, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('chain', 'next'),
    )


# あるバージョンの先行を追跡できること
# 1
next_succession = aliased(Succession)
nexts = session.query(Succession, next_succession)\
    .join(next_succession, and_(
        Succession.next + 1 == next_succession.next,
        Succession.chain == next_succession.chain)
    )
[print(s.chain, s.file_id, n_s.file_id) for s, n_s in nexts]

# 2
nexts = session.query(Succession, next_succession).filter(and_(
    Succession.next + 1 == next_succession.next,
    Succession.chain == next_succession.chain
))

[print(s.chain, s.file_id, n_s.file_id) for s, n_s in nexts]

# あるバージョンの後続を追跡できること
prev_succession = aliased(Succession)
prevs = session.query(Succession, prev_succession).filter(and_(
    Succession.next == prev_succession.next + 1,
    Succession.chain == prev_succession.chain
))

[print(s.chain, s.file_id, n_s.file_id) for s, n_s in prevs]

# 最新バージョン
# DISTINCT + CROSS JOIN はできないようだ。
chain_succession = aliased(Succession)
latest_succession = Query([func.max(chain_succession.next)]).filter(chain_succession.chain == Succession.chain).subquery()
latests = session.query(Succession, Portfolio).filter(and_(
    Succession.file_id == Portfolio.file_id,
    Succession.next == latest_succession
))

[print(p.stuff) for s, p in latests]

# 監査証跡
[print(s.chain, s.file_id) for s in session.query(Succession).order_by(Succession.chain, Succession.next)]
