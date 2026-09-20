SELECT
    CAST(date AS TIMESTAMP) AS date,
    CAST(year AS INTEGER) AS year,
    CAST(month AS INTEGER) AS month,
    CAST(day AS INTEGER) AS day,
    CAST(day_of_week AS INTEGER) AS day_of_week,
    CAST(is_weekend AS BOOLEAN) AS is_weekend
FROM {{ source('shopops_raw', 'calendar') }}
