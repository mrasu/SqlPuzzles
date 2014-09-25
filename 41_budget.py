from sqlalchemy import Column, Integer, String, Float, func, case, or_
from sqlalchemy.orm import Query
from util import Base, session


class Items(Base):
    __tablename__ = "items"

    item_nbr = Column(Integer, primary_key=True)
    item_descr = Column(String)


class Estimates(Base):
    __tablename__ = "estimates"

    item_nbr = Column(Integer, primary_key=True)
    estimated_amt = Column(Float)


class Actuals(Base):
    __tablename__ = "actuals"

    item_nbr = Column(Integer, primary_key=True)
    actual_amt = Column(Float)
    check_nbr = Column(String)

actual_sum = Query(func.sum(Actuals.actual_amt)).filter(Actuals.item_nbr == Items.item_nbr).as_scalar()
estimate_sum = Query(func.sum(Estimates.estimated_amt)).filter(Estimates.item_nbr == Items.item_nbr).as_scalar()
check_number = Query([case([(func.count(Actuals.item_nbr) == 1, func.max(Actuals.check_nbr))], else_="Mixed")])\
    .filter(Actuals.item_nbr == Items.item_nbr).group_by(Actuals.item_nbr).as_scalar()
print("\r\nresult*****")
result = session.query(Items, actual_sum, estimate_sum, check_number).filter(or_(actual_sum != None, estimate_sum != None)).all()
print(result)