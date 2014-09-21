# JOIN型
SELECT
    badges.emp_id,
    badges.badge_nbr
FROM
    badges
    INNER JOIN (
       SELECT
           emp_id,
           max(issued_date) AS issued_data
       FROM badges
       GROUP BY emp_id
   ) AS available_badges ON badges.emp_id = available_badges.emp_id AND badges.issued_date = available_badges.issued_data;


# 相関サブクエリ
SELECT
    *
FROM badges
WHERE badge_seq = (
    SELECT
        max(badge_seq)
    FROM badges AS active_badges
    WHERE active_badges.emp_id = badges.emp_id);
