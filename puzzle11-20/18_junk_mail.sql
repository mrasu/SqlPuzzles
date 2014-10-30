SELECT
  *
FROM consumers
WHERE
  consumers.fam IS NULL AND
  exists(SELECT
           address
         FROM consumers AS consumers2
         WHERE
           consumers.address = consumers2.address
         HAVING count(*) > 1);

SELECT
  *
FROM consumers
  INNER JOIN consumers AS consumers2 ON consumers.address = consumers2.address AND consumers.con_id <> consumers2.con_id
WHERE
  consumers.fam IS NULL;
