WITH products AS (
    SELECT * FROM {{ ref('stg_products_scd2') }}
)

SELECT
    product_id,
    product_name,
    price AS unit_price_eur,
    start_date,
    end_date,
    -- Création d'un flag pour repérer facilement le prix actuel
    CASE
        WHEN end_date >= CURRENT_TIMESTAMP THEN true
        ELSE false
    END AS is_active
FROM products
