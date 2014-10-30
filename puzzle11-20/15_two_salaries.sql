SELECT
  *
FROM
  salaries
  LEFT OUTER JOIN salaries AS previous_salary
    ON salaries.emp_name = previous_salary.emp_name AND salaries.sal_date > previous_salary.sal_date AND
       salaries.sal_amt <> previous_salary.sal_amt
WHERE
  salaries.sal_date = (
    SELECT
      max(sal_date)
    FROM salaries AS latest_salary
    WHERE
      latest_salary.emp_name = salaries.emp_name) AND
  (previous_salary.sal_date = (
    SELECT
      max(a.sal_date)
    FROM salaries AS a
    WHERE
      a.sal_date < salaries.sal_date AND a.emp_name = salaries.emp_name) OR previous_salary.emp_name IS NULL);