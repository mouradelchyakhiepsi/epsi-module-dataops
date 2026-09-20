SELECT
    CAST(date AS TIMESTAMP) AS date,
    CAST(currency_from AS VARCHAR) AS currency_from,
    CAST(currency_to AS VARCHAR) AS currency_to,
    CAST(rate AS DOUBLE) AS rate
FROM {{ source('shopops_raw', 'exchange_rates') }}
