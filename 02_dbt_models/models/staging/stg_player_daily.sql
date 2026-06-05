WITH wellness AS (
    SELECT * FROM {{ ref('base_wellness') }}
),
load AS (
    SELECT * FROM {{ ref('base_training_load') }}
)
SELECT
    w.date,
    w.player_id,
    w.team,
    w.fatigue,
    w.mood,
    w.readiness,
    w.sleep_duration,
    w.sleep_quality,
    w.soreness,
    w.stress,
    ROUND((
        (8 - COALESCE(w.fatigue, 4)) +
        COALESCE(w.mood, 4) +
        COALESCE(w.readiness, 5) +
        COALESCE(w.sleep_quality, 4) +
        (8 - COALESCE(w.soreness, 4)) +
        (8 - COALESCE(w.stress, 4))
    ) / 6.0, 2)                 AS wellness_score,
    l.daily_load,
    l.weekly_load,
    l.acwr,
    l.atl,
    l.ctl28,
    l.strain,
    l.monotony
FROM wellness w
LEFT JOIN load l
    ON  w.date      = l.date
    AND w.player_id = l.player_id