SELECT
    date,
    player_id,
    team,
    wellness_score,
    acwr,
    daily_load,
    weekly_load,
    fatigue,
    mood,
    readiness,
    sleep_duration,
    sleep_quality,
    soreness,
    stress,
    CASE
        WHEN wellness_score >= 6.0 AND (acwr BETWEEN 0.8 AND 1.3 OR acwr IS NULL)
            THEN 'Ready'
        WHEN wellness_score >= 4.5 OR acwr BETWEEN 0.6 AND 1.5
            THEN 'Monitor'
        ELSE 'Load-Managed'
    END AS readiness_status
FROM {{ ref('stg_player_daily') }}
WHERE date IS NOT NULL