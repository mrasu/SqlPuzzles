
SELECT
    claims.*,
    min(claim_seq)
FROM
    (
        SELECT
            legalevents.claim_id,
            legalevents.defendant_name,
            max(claimstatuscodes.claim_seq) AS claim_seq
        FROM
            legalevents
            INNER JOIN claimstatuscodes ON legalevents.claim_status = claimstatuscodes.claim_status
        GROUP BY
            legalevents.claim_id,
            legalevents.defendant_name
    ) AS claim_status
    INNER JOIN claims ON claim_status.claim_id = claims.claim_id
GROUP BY
    claims.claim_id;
