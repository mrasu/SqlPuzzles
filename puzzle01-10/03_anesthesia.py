#encoding: utf-8

from sqlalchemy import Column, Integer, String, DateTime, and_, not_, or_, select
from sqlalchemy.orm import Query, aliased
from util import Base, session


#TODO 未完成
"""
SELECT sum(subquery)が出来なかった
"""
class Procs(Base):
    __tablename__ = "Procs"

    proc_id = Column(Integer, primary_key=True)
    anest_name = Column(String(40))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

# 開始時に+1, 終了時に-1することにより任意の時間までの合計ポイント = 対象時間の処置数
procs2 = aliased(Procs, name="Procs2")
events = Query([
    Procs.proc_id.label("proc_id"),
    Procs.anest_name.label("anest_name"),
    procs2.start_time.label("event_time"),
    select([1]).label("event_type")
]).join(procs2, Procs.anest_name == procs2.anest_name). \
    filter(
        not_(or_(procs2.end_time <= Procs.start_time, procs2.start_time >= Procs.end_time))
    ).union_all(
        Query([Procs.proc_id, Procs.anest_name, procs2.end_time, "-1"]).
        join(procs2, Procs.anest_name == procs2.anest_name)
        .filter(
            not_(or_(procs2.end_time <= Procs.start_time, procs2.start_time >= Procs.end_time))
        )
    )

print(events)

print("*******\r\n")

events2 = aliased(events.subquery())
a = Query([sum(events.event_type)])

procs_sum = select([events.c.proc_id, events.c.event_time,
    select([events2.c.event_type], events.c.proc_id == events2.c.proc_id ).label("instantaneous_count")
])

print(procs_sum)
"""
SELECT E1.proc_id, E1.event_time,
    (SELECT sum(E2.event_type)
        FROM Events AS E2
        WHERE E2.proc_id = E1.proc_id
            AND E2.event_time < E1.event_time
    ) AS instantaneous_count
FROM Events AS E1
    ORDER BY E1.proc_id, E1.event_time;
"""
