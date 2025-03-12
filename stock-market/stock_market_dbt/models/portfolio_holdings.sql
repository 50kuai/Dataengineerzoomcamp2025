{{ config(schema='dbt_stock_project', materialized='table') }}

WITH latest_date AS (
    SELECT MAX(date) AS max_date
    FROM {{ source('stock_dataset', 'transactions') }}
),

transactions AS (
    SELECT
        date,
        ticker,
        quantity,
        type
    FROM {{ source('stock_dataset', 'transactions') }}
    WHERE date = (SELECT max_date FROM latest_date)
)

SELECT
    ticker,
    SUM(CASE WHEN type = 'BUY' THEN quantity ELSE -quantity END) AS total_shares
FROM transactions
GROUP BY ticker