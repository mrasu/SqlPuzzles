SELECT
    *
FROM (
         SELECT
             I1.item_nbr,
             I1.item_descr,
             (
                 SELECT
             sum(A1.actual_amt)
                 FROM actuals AS A1
                 WHERE I1.item_nbr = A1.item_nbr) AS tot_act,
             (
                 SELECT
             sum(E1.estimated_amt)
                 FROM estimates AS E1
                 WHERE I1.item_nbr = E1.item_nbr
             )                                    AS tot_estimate,
             (
                 SELECT
             CASE WHEN count(*) = 1 THEN max(check_nbr)
             ELSE 'Mixed' END
                 FROM actuals AS A2
                 WHERE I1.item_nbr = A2.item_nbr
                 GROUP BY item_nbr
             )                                    AS check_nbr
         FROM items AS I1
     ) AS TMP
WHERE tot_act IS NOT NULL OR tot_estimate IS NOT NULL;

