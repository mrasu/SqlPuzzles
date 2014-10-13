# EXISTSで場合分け
SELECT
    *
FROM
    printercontrol
WHERE CASE WHEN exists(
        SELECT
           *
       FROM printercontrol
       WHERE user_id = 'lee'
    ) THEN
        user_id = 'lee'
    ELSE
        user_id IS NULL
    END;

# 集計関数がNULLを返すことを利用する
SELECT
    coalesce(min(printer_name), (
        SELECT
            min(printer_name)
        FROM printercontrol AS P2
        WHERE user_id IS NULL))
FROM printercontrol AS P1
WHERE user_id = 'lee';

