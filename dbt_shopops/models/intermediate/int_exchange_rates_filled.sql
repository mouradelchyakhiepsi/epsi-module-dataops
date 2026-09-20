WITH calendar AS (
    SELECT date FROM {{ ref('stg_calendar') }}
),

rates AS (
    SELECT date, currency_to, rate
    FROM {{ ref('stg_exchange_rates') }}
),

currencies AS (
    SELECT DISTINCT currency_to FROM rates
),

-- On crée une ligne pour chaque jour et chaque devise possible
calendar_currencies AS (
    SELECT
        c.date,
        cur.currency_to
    FROM calendar c
    CROSS JOIN currencies cur
),

-- On ramène les taux connus (ce qui crée des NULLs le week-end)
joined_rates AS (
    SELECT
        cc.date,
        cc.currency_to,
        r.rate
    FROM calendar_currencies cc
    LEFT JOIN rates r
        ON cc.date = r.date
        AND cc.currency_to = r.currency_to
),

-- On utilise le fenêtrage pour combler les trous (Forward Fill)
filled_rates AS (
    SELECT
        date,
        currency_to,
        last_value(rate) IGNORE NULLS OVER (
            PARTITION BY currency_to
            ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS active_rate
    FROM joined_rates
)

SELECT * FROM filled_rates
