SELECT
    CAST(date AS DATE)          AS date,
    player_id,
    team,
    CAST(daily_load AS FLOAT)   AS daily_load,
    CAST(weekly_load AS FLOAT)  AS weekly_load,
    CAST(acwr AS FLOAT)         AS acwr,
    CAST(atl AS FLOAT)          AS atl,
    CAST(ctl28 AS FLOAT)        AS ctl28,
    CAST(strain AS FLOAT)       AS strain,
    CAST(monotony AS FLOAT)     AS monotony
FROM read_parquet('../data/processed/training_load.parquet')