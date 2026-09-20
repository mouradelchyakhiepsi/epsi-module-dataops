SELECT
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(product_name AS VARCHAR) AS product_name,
    CAST(price AS DOUBLE) AS price,
    CAST(start_date AS TIMESTAMP) AS start_date,
    CAST(end_date AS TIMESTAMP) AS end_date
FROM {{ source('shopops_raw', 'products_scd2') }}
