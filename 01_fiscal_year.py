from sqlalchemy import create_engine, Column, Integer, Date, CheckConstraint
from sqlalchemy.exc import InternalError
from sqlalchemy.ext.declarative import declarative_base

"""
敗北に満ちた文字列制約
"""


engine = create_engine("mysql+pymysql://root@localhost/sql_puzzles", echo=True)

Base = declarative_base()


# 日付決め打ち
class FiscalYearTable1(Base):
    __tablename__ = "FiscalYearTable1"

    fiscal_year = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("(EXTRACT(YEAR FROM start_date) = fiscal_year + 1) AND "
                        "(EXTRACT(MONTH FROM start_date) = 10) AND "
                        "(EXTRACT(DAY FROM start_date) = 1)", name="valid_start_date"),
        CheckConstraint("(EXTRACT(YEAR FROM end_date) = fiscal_year) AND"
                        "(EXTRACT(MONTH FROM end_date) = 9) AND"
                        "(EXTRACT(DAY FROM end_date) = 30)", name="valid_end_date"),
    )


# 1年チェック
class FiscalYearTable2(Base):
    __tablename__ = "FiscalYearTable2"

    fiscal_year = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "ADDDATE(start_date, INTERVAL 1 YEAR) = ADDDATE(end_date, INTERVAL 1 DAY)",
            name="valid_one_year"),
    )


# 52週チェック
# 1年チェック
class FiscalYearTable3(Base):
    __tablename__ = "FiscalYearTable3"

    fiscal_year = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "DATEDIFF(end_date, start_date) = 359",
            name="valid_52_weeks"),
    )

try:
    FiscalYearTable1.__table__.drop(engine)
except InternalError:
    pass

try:
    FiscalYearTable2.__table__.drop(engine)
except InternalError:
    pass

try:
    FiscalYearTable3.__table__.drop(engine)
except InternalError:
    pass

Base.metadata.create_all(engine)
