SELECT
  *
FROM
  personnel
  LEFT OUTER JOIN
  (
    SELECT
      *
    FROM
      phones
    WHERE
      phone_type = 'hom') AS hom_phones
    ON personnel.emp_id = hom_phones.emp_id
  LEFT OUTER JOIN
  (
    SELECT
      *
    FROM
      phones
    WHERE
      phone_type = 'fax'
  ) AS fax_phones
    ON personnel.emp_id = fax_phones.emp_id;


SELECT
  personnel.emp_id,
  max(CASE WHEN phones.phone_type = 'hom' THEN phones.phone_nbr END),
  max(CASE WHEN phones.phone_type = 'fax' THEN phones.phone_nbr END)
FROM personnel
  LEFT OUTER JOIN phones ON personnel.emp_id = phones.emp_id
GROUP BY
  emp_id;


