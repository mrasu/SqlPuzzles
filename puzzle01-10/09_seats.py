# encoding:utf-8
from sqlalchemy import Column, Integer, not_, func
from sqlalchemy.orm import Query, aliased
from util import Base, session


class Restaurant(Base):
    __tablename__ = "restaurant"

    seat = Column(Integer, primary_key=True)

# 空きの最初と最後を求めれば、間は空席
#TODO next_last_seatのfirst_seatが相関にならなくてエラー。後で治す
"""
first_seat = Query([Restaurant.seat.label("seat")]).filter(
    not_(Restaurant.seat.in_(
        Query([Restaurant.seat - 1]).subquery()
    ))
).subquery()

last_seat = Query([Restaurant.seat.label("seat")]).filter(
    not_(Restaurant.seat.in_(
        Query([Restaurant.seat + 1]).subquery()
    ))
).subquery()

next_last_seat = Query([func.min(last_seat.c.seat)]).filter(first_seat.c.seat + 1 <= last_seat.c.seat - 1).as_scalar()

seat = session.query(first_seat, last_seat).filter(last_seat.c.seat - 1 == next_last_seat)
[print(s) for s in seat]
"""

# 自己結合により、次の席を求める
first = aliased(Restaurant)
last = aliased(Restaurant)
seat = session.query(first.seat + 1, func.min(last.seat)).join(last, first.seat < last.seat)\
    .group_by(first.seat).having(first.seat < func.min(last.seat - 1))
[print(s) for s in seat]
