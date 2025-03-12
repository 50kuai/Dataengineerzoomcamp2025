{{ config(schema='dbt_stock_project', materialized='table') }}

WITH latest_date AS (
    SELECT MAX(date) AS max_date
    FROM {{ source('stock_dataset', 'stock_data') }}
),

stock_data AS (
    SELECT
        date,
        ticker,
        close
    FROM {{ source('stock_dataset', 'stock_data') }}
    WHERE date = (SELECT max_date FROM latest_date)
),

holdings AS (
    SELECT
        ticker,
        total_shares
    FROM {{ ref('portfolio_holdings') }}
)

SELECT
    h.ticker,
    h.total_shares,
    sd.close AS close_price,
    h.total_shares * sd.close AS market_value
FROM holdings h
JOIN stock_data sd ON h.ticker = sd.ticker