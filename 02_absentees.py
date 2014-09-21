import datetime
from sqlalchemy import create_engine, Column, Integer, Date, CheckConstraint, String, func, case, outerjoin, and_
from sqlalchemy.exc import InternalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased, Query


engine = create_engine("mysql+pymysql://root@localhost/sql_puzzles", echo=True)

Base = declarative_base()


class Absenteeism(Base):
    __tablename__ = "Absenteeism"

    id = Column(Integer, primary_key=True)
    emp_id = Column(Integer, nullable=True)
    absent_date = Column(Date, nullable=False)
    severity_points = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Absenteeism: emp_id={}, absent_date={}, severity_points={}".format(self.emp_id, self.absent_date, self.severity_points)


class Calendar(Base):
    __tablename__ = "Calendar"

    cal_date = Column(Date, primary_key=True)

try:
    Absenteeism.__table__.drop(engine)
except InternalError:
    pass



Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

session.add_all([
    Absenteeism(emp_id=1, absent_date=datetime.date(2014, 1, 1), severity_points=4),
    Absenteeism(emp_id=1, absent_date=datetime.date(2014, 1, 2), severity_points=2),
    Absenteeism(emp_id=1, absent_date=datetime.date(2014, 1, 3), severity_points=3),
    Absenteeism(emp_id=2, absent_date=datetime.date(2014, 1, 1), severity_points=1),
    Absenteeism(emp_id=2, absent_date=datetime.date(2014, 1, 3), severity_points=2),
    Absenteeism(emp_id=2, absent_date=datetime.date(2014, 1, 4), severity_points=3)
])

# SELECTで出す型
abs2 = aliased(Absenteeism)
sum_scalar = func.sum(case([(abs2.emp_id == None, Absenteeism.severity_points)], else_=0))
q = Query([Absenteeism.emp_id, sum_scalar])\
    .outerjoin(abs2, and_(Absenteeism.emp_id == abs2.emp_id, Absenteeism.absent_date - abs2.absent_date == 1))\
    .group_by(Absenteeism.emp_id)\
    .having(sum_scalar >= 40)

print(q)

# UPDATEで効率よくいく型
# UPDATE中にJOINが使え無いようなのでできない・・
for absentee in session.query(Absenteeism).join(abs2, and_(
        Absenteeism.emp_id == abs2.emp_id,
        func.datediff(Absenteeism.absent_date, abs2.absent_date) == 1)).all():
    absentee.severity_points = 0

q = Query(Absenteeism).join(Calendar, Absenteeism.absent_date == Calendar.cal_date)\
    .group_by(Absenteeism.emp_id).having(func.sum(Absenteeism.severity_points) >= 40)

print(q)