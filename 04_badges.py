from sqlalchemy import Column, Integer, Date, UniqueConstraint, func, and_, select
from sqlalchemy.orm import Query, aliased
from util import Base, session


class Badges(Base):
    __tablename__ = "badges"

    badge_nbr = Column(Integer, primary_key=True)
    emp_id = Column(Integer, nullable=False)
    issued_date = Column(Date, nullable=False)
    badge_seq = Column(Integer)

    __table_args__ = (
        UniqueConstraint('badge_seq'),
    )

# JOIN型
available_badges_query = aliased(
    Query([Badges.emp_id, func.max(Badges.issued_date).label("issued_date")]).group_by(Badges.emp_id).subquery()
)

available_badges = session.query(Badges).join(
    available_badges_query,
    and_(
        Badges.emp_id == available_badges_query.c.emp_id,
        Badges.issued_date == available_badges_query.c.issued_date,
    )
).all()

print([(b.emp_id, b.issued_date) for b in available_badges])

# 相関サブクエリ
active_badges = aliased(Badges)
max_badge_seq = Query([func.max(active_badges.badge_seq)]).filter(active_badges.emp_id == Badges.emp_id)
available_badges = session.query(Badges).filter(Badges.badge_seq == max_badge_seq)

print([(b.emp_id, b.issued_date) for b in available_badges])
