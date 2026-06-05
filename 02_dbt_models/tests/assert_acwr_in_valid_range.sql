-- This test passes if it returns 0 rows
-- Flags any ACWR value outside the expected 0-5 range
SELECT *
FROM {{ ref('mart_injury_risk') }}
WHERE acwr < 0 OR acwr > 5