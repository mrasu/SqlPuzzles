# 開始時に+1, 終了時に-1することにより任意の時間までの合計ポイント = 対象時間の処置数
CREATE VIEW Events
(proc_id, comparison_proc, anest_name, event_time, event_type) AS
    SELECT
        P1.proc_id,
        P2.proc_id,
        P1.anest_name,
        P2.start_time,
        +1 AS event_type
    FROM procs AS P1, procs AS P2
    WHERE P1.anest_name = P2.anest_name
          AND NOT (P2.end_time <= P1.start_time
                   OR P2.start_time >= P1.end_time)
    UNION
    SELECT
        P1.proc_id,
        P2.proc_id,
        P1.anest_name,
        P2.end_time,
        -1 AS event_type
    FROM procs AS P1, procs AS P2
    WHERE P1.anest_name = P2.anest_name
          AND NOT (P2.end_time <= P1.start_time
                   OR P2.start_time >= P1.end_time);


select E1.proc_id, E1.event_time,
    (select sum(E2.event_type)
        from Events as E2
        where E2.proc_id = E1.proc_id
            and E2.event_time < E1.event_time
    ) as instantaneous_count
from Events as E1
    order by E1.proc_id, E1.event_time;


# ある時点での処置数を見る時の解
# 処置の開始時点に必ず最大数があることを応用し、P2で開始時点、P3でP2の開始時間にまたがる処置を置くことで最大数を見出している。
# きれい
CREATE VIEW Vprocs(id1, id2, total) AS
    SELECT
        P1.proc_id,
        P2.proc_id,
        count(*)
    FROM procs AS P1, procs AS P2, procs AS P3
    WHERE
        P2.anest_name = P1.anest_name
        AND P3.anest_name = P1.anest_name
        AND P1.start_time <= P2.start_time
        AND P2.start_time < P1.end_time
        AND P3.start_time <= P2.start_time
        AND P2.start_time < P3.end_time
    GROUP BY P1.proc_id, P2.proc_id;

select * from Vprocs;

select id1 as proc_id, max(total) as max_inst_count
from vprocs
    group by id1;