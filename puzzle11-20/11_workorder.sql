# 素直に解く
SELECT
    workorder_id
FROM projects
GROUP BY workorder_id
HAVING sum(CASE WHEN step_status = 'C' AND step_nbr = 0 THEN 1
           WHEN step_status = 'W' AND step_nbr <> 0 THEN 1
           ELSE 0 END) = count(*);

# 0以外はみんな待ち
SELECT
    workorder_id
FROM projects AS P1
WHERE step_nbr = 0 AND step_status = 'C' AND 'W' = ALL (
    SELECT
        step_status
    FROM projects AS P2
    WHERE P2.workorder_id = P1.workorder_id AND P2.step_nbr <> 0);

# SUMが0なら、最初だけ
SELECT
    workorder_id
FROM projects
WHERE step_status = 'C'
GROUP BY workorder_id
HAVING 0 = sum(step_nbr);
