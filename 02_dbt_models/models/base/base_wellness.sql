SELECT
    CAST(date AS DATE)            AS date,
    player_id,
    team,
    CAST(fatigue AS FLOAT)        AS fatigue,
    CAST(mood AS FLOAT)           AS mood,
    CAST(readiness AS FLOAT)      AS readiness,
    CAST(sleep_duration AS FLOAT) AS sleep_duration,
    CAST(sleep_quality AS FLOAT)  AS sleep_quality,
    CAST(soreness AS FLOAT)       AS soreness,
    CAST(stress AS FLOAT)         AS stress
FROM read_parquet('../data/processed/wellness.parquet')