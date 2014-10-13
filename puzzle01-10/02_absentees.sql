# SELECTで出す型
SELECT
    ab1.emp_id,
    sum(
        CASE WHEN ab2.emp_id IS NULL THEN ab1.severity_points
        ELSE 0 END
    ) AS point
FROM
    absenteeism AS ab1
    LEFT OUTER JOIN absenteeism AS ab2
        ON ab1.emp_id = ab2.emp_id AND ab1.absent_date - ab2.absent_date = 1
GROUP BY
    ab1.emp_id;


# UPDATEで効率よくいく型
update absenteeism
    cross join absenteeism as a2
set
    absenteeism.severity_points = 0,
    absenteeism.reason_code = 'long term illness'
where absenteeism.emp_id = a2.emp_id and
          datediff(a2.absent_date, absenteeism.absent_date) =1;

SELECT
    *
FROM absenteeism
    CROSS JOIN calendar
WHERE calendar.cal_date = absenteeism.absent_date
GROUP BY absenteeism.emp_id
HAVING sum(severity_points) >= 40;
