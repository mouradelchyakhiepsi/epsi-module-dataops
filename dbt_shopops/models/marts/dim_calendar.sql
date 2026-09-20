WITH calendar AS (
    SELECT * FROM {{ ref('stg_calendar') }}
)

SELECT
    date,
    year,
    month,
    day,
    day_of_week,
    is_weekend,
    -- Ajout pédagogique : on enrichit pour faciliter la vie des analystes BI
    EXTRACT(QUARTER FROM date) AS quarter,
    CASE
        WHEN is_weekend = true THEN 'Week-end'
        ELSE 'Semaine'
    END AS day_type
FROM calendar
