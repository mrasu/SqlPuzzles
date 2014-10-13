from sqlalchemy import Column, Integer, String, func, case, and_
from sqlalchemy.orm import aliased, Query
from util import Base, session


class Project(Base):
    __tablename__ = "projects"

    workorder_id = Column(String(5), primary_key=True)
    step_nbr = Column(Integer, nullable=False, primary_key=True)
    step_status = Column(String(1), nullable=False)

print(session.query(Project).all())

# 素直に解く
work_order = session.query(Project.workorder_id).group_by(Project.workorder_id)\
    .having(func.count() == func.sum(case(
        [
            (and_(Project.step_status == "C", Project.step_nbr == 0), 1),
            (and_(Project.step_status == "W", Project.step_nbr != 0), 1)
        ],
        else_=0
    )))

print(work_order.all())

# TODO また自己参照
# 0以外はみんな待ち
"""
project1 = aliased(Project)
project2 = Query([project1.step_status]).filter(project1.step_status == Project.step_status).subquery()

work_order = session.query(Project).filter(Project.step_status == func.max(project2.c.step_status))

"""

# SUMが0なら、最初だけ
work_order = session.query(Project.workorder_id).filter(Project.step_status == "C").group_by(Project.workorder_id).having(func.sum(Project.step_nbr) == 0)
print(work_order)
