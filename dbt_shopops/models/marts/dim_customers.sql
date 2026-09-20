WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)

SELECT
    customer_id,
    name AS customer_name,
    country,
    signup_date
FROM customers
