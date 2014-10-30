SELECT
  candidateskills.candidate_id,
  joborders.job_id
FROM candidateskills
  INNER JOIN joborders ON candidateskills.skill_code = joborders.skill_code
GROUP BY
  candidateskills.candidate_id,
  joborders.job_id
HAVING count(*) = (
  SELECT
    count(*)
  FROM joborders AS target_job
  WHERE
    target_job.job_id = joborders.job_id);
