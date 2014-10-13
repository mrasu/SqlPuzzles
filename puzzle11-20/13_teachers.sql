SELECT
  course_nbr,
  min(teacher_name),
  CASE WHEN count(*) = 1 THEN ''
  WHEN count(*) = 2 THEN max(teacher_name)
  ELSE '--More--' END AS teacher_name2
FROM register
GROUP BY course_nbr;