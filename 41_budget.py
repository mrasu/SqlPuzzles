from sqlalchemy import Column, Integer, String, create_engine, Float, func, case, select, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query

engine = create_engine("sqlite:///:memory:", echo=False)

Base = declarative_base()


class Items(Base):
    __tablename__ = "items"

    item_number = Column(Integer, primary_key=True)
    item_descripttion = Column(String)


class Estimates(Base):
    __tablename__ = "estimates"

    item_number = Column(Integer, primary_key=True)
    estimated_amount = Column(Float)


class Actuals(Base):
    __tablename__ = "actuals"

    item_number = Column(Integer, primary_key=True)
    actual_amount = Column(Float)
    check_number = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

actual_sum = Query(func.sum(Actuals.actual_amount)).filter(Actuals.item_number == Items.item_number).as_scalar()
estimate_sum = Query(func.sum(Estimates.estimated_amount)).filter(Estimates.item_number == Items.item_number).as_scalar()
check_number = Query(case([(func.count(Actuals), func.max(Actuals.check_number))], else_="Mixed")).\
    group_by(Actuals.item_number).filter(Actuals.item_number == Items.item_number).as_scalar()

print("\r\nresult*****")
result = Query([Items, actual_sum, estimate_sum, check_number]).filter(or_(actual_sum != None, estimate_sum != None))
print(result)