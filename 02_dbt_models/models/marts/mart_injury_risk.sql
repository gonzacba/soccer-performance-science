SELECT
    date,
    player_id,
    team,
    acwr,
    atl,
    ctl28,
    wellness_score,
    daily_load,
    strain,
    monotony,
    CASE
        WHEN acwr > 1.5                             THEN 'High'
        WHEN acwr > 1.3 OR wellness_score < 4.0    THEN 'Elevated'
        ELSE                                             'Normal'
    END AS risk_level,
    CASE
        WHEN acwr > 1.5 THEN TRUE
        ELSE FALSE
    END AS acwr_spike_flag
FROM {{ ref('stg_player_daily') }}
WHERE acwr IS NOT NULL