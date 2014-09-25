# あるバージョンの先行を追跡できること
# 1
SELECT
    succession.chain,
    succession.file_id,
    next_succession.file_id AS next_file_id
FROM
    succession
    INNER JOIN succession AS next_succession ON
         succession.next + 1 = next_succession.next AND
         succession.chain = next_succession.chain;

# 2
SELECT
    succession.chain,
    succession.file_id,
    next_succession.file_id AS next_file_id
FROM
    succession, succession AS next_succession
WHERE
    succession.next + 1 = next_succession.next AND
    succession.chain = next_succession.chain;


# あるバージョンの後続を追跡できること
SELECT
    succession.chain,
    succession.file_id,
    prev_succession.file_id as prev_file_id
FROM
    succession, succession AS prev_succession
WHERE
    succession.next = prev_succession.next + 1 AND
    succession.chain = prev_succession.chain;

# 最新バージョン
SELECT distinct
    portfolios.*
FROM
    succession,
    portfolios
WHERE
    succession.file_id = portfolios.file_id AND
    succession.file_id = (
        SELECT
            max(chain_succession.file_id)
        FROM
            succession AS chain_succession
        WHERE
            chain_succession.chain = succession.chain
    );

# 監査証跡
SELECT
    *
FROM
    succession
ORDER BY
    chain,
    next;

