# encoding:utf-8

from sqlalchemy import Column, String, case, func
from sqlalchemy.orm import Query
from sqlalchemy.sql.functions import coalesce
from util import Base, session


class PrinterControl(Base):
    __tablename__ = "printercontrol"

    user_id = Column(String(10))
    printer_name = Column(String(4), nullable=False, primary_key=True)
    printer_description = Column(String(40), nullable=False)

user_name = "leea"
user_printer = Query([PrinterControl]).filter(PrinterControl.user_id == user_name)
s = session.query(PrinterControl).filter(case(
    [(user_printer.exists(), PrinterControl.user_id == user_name)],
    else_=(PrinterControl.user_id == None))
)

[print(s.printer_name) for s in s]


# 集計関数がNULLを返すことを利用する
anonymous_printer = Query([func.min(PrinterControl.printer_name)])\
    .filter(PrinterControl.user_id == None).as_scalar()

s = session.query(coalesce(func.min(PrinterControl.printer_name), anonymous_printer))\
    .filter(PrinterControl.user_id == user_name)

[print(s) for s in s]
