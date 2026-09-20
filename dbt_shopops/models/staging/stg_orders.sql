SELECT
    CAST(order_id AS VARCHAR) AS order_id,
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(order_date AS TIMESTAMP) AS order_date,
    CAST(status AS VARCHAR) AS status
FROM {{ source('shopops_raw', 'raw_orders') }}
