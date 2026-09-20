WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products_scd2') }}
),

enriched_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.product_id,
        o.quantity,
        o.order_date,
        o.status,
        p.product_name,
        p.price AS unit_price
    FROM orders o
    LEFT JOIN products p
        ON o.product_id = p.product_id
        -- La magie du SCD2 : la commande doit tomber pendant la période de validité du prix
        AND o.order_date >= p.start_date
        AND o.order_date < p.end_date
)

SELECT * FROM enriched_orders
