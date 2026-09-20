WITH orders AS (
    SELECT * FROM {{ ref('int_orders_enriched') }}
),

payments AS (
    SELECT * FROM {{ ref('stg_payments') }}
),

exchange_rates AS (
    SELECT * FROM {{ ref('int_exchange_rates_filled') }}
),

-- On agrège les paiements au cas où une commande serait payée en plusieurs fois
order_payments AS (
    SELECT
        order_id,
        MAX(currency) AS payment_currency,
        SUM(amount) AS total_paid_local
    FROM payments
    GROUP BY order_id
),

final AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.product_id,
        o.order_date,
        o.status AS order_status,
        o.quantity,
        o.unit_price AS unit_price_eur,
        -- Calcul du chiffre d'affaires théorique de la commande
        (o.quantity * o.unit_price) AS order_amount_eur,

        op.payment_currency,
        op.total_paid_local,

        -- Conversion du paiement réel en EUR en utilisant le taux de change actif à la date de la commande
        (op.total_paid_local / COALESCE(er.active_rate, 1.0)) AS total_paid_eur

    FROM orders o
    LEFT JOIN order_payments op
        ON o.order_id = op.order_id
    LEFT JOIN exchange_rates er
        -- On fait correspondre la date et la devise pour appliquer le bon taux
        ON DATE(o.order_date) = DATE(er.date)
        AND op.payment_currency = er.currency_to
)

SELECT * FROM final
