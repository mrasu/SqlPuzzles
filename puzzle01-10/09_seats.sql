# 空きの最初と最後を求めれば、間は空席
SELECT
    *
FROM
    (
        SELECT
            seat + 1 AS seat
        FROM restaurant
        WHERE seat + 1 NOT IN (
            SELECT
                seat
            FROM restaurant) AND seat < 1000) AS first_seats,
    (

        SELECT
            seat - 1 AS seat
        FROM restaurant
        WHERE seat - 1 NOT IN (
            SELECT
                seat
            FROM restaurant) AND seat > 0
    ) AS last_seats
WHERE
    first_seats.seat <= last_seats.seat AND
    last_seats.seat = (
        SELECT
            min(seat - 1)
        FROM restaurant
        WHERE seat - 1 NOT IN (
            SELECT
                seat
            FROM restaurant) AND first_seats.seat <= seat);

# 自己結合により、次の席を求める
SELECT
    first.seat + 1,
    min(last.seat - 1)
FROM restaurant AS first INNER JOIN restaurant AS last ON first.seat < last.seat
GROUP BY first.seat
HAVING first.seat < min(last.seat - 1);



