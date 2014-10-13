# 日付決め打ち
CREATE TABLE FiscalYearTable1
(
    fiscal_year INTEGER PRIMARY KEY,
    start_date DATE NOT NULL ,
    CONSTRAINT valid_start_date
        CHECK ((EXTRACT(YEAR FROM start_date) = fiscal_year + 1) AND
               (EXTRACT(MONTH FROM start_date) = 10) AND
               (EXTRACT(DAY FROM start_date) = 1)
    ),
    end_date DATE NOT NULL ,
    CONSTRAINT valid_end_date
        CHECK((EXTRACT(YEAR FROM end_date) = fiscal_year) AND
              (EXTRACT(MONTH FROM end_date) = 9) AND
              (EXTRACT(DAY FROM end_date) = 30)
    )
);

# 1年チェック
CREATE TABLE FiscalYearTable2
(
    fiscal_year INTEGER PRIMARY KEY,
    start_date DATE NOT NULL ,
    end_date DATE NOT NULL ,
    CONSTRAINT valid_one_year
        CHECK(ADDDATE(start_date, INTERVAL 1 YEAR) = ADDDATE(end_date, INTERVAL 1 DAY))
);

# 359日制約
CREATE TABLE FiscalYearTable3
(
    fiscal_year INTEGER PRIMARY KEY,
    start_date DATE NOT NULL ,
    end_date DATE NOT NULL ,
    CONSTRAINT valid_52_weeks
        CHECK(DATEDIFF(end_date, start_date) = 359)
);