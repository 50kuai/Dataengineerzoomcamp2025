{{ config(schema='dbt_stock_project', materialized='table') }}

WITH dates AS (
    SELECT DISTINCT date
    FROM {{ source('stock_dataset', 'stock_data') }}
),

tickers AS (
    SELECT DISTINCT ticker
    FROM {{ source('stock_dataset', 'stock_data') }}
),

date_ticker_combinations AS (
    SELECT
        d.date,
        t.ticker
    FROM dates d
    CROSS JOIN tickers t
),

transactions AS (
    SELECT
        date,
        ticker,
        quantity,
        price,
        type
    FROM {{ source('stock_dataset', 'transactions') }}
),

daily_holdings AS (
    SELECT
        dt.date,
        dt.ticker,
        SUM(CASE WHEN t.type = 'BUY' THEN t.quantity ELSE 0 END) - SUM(CASE WHEN t.type = 'SELL' THEN t.quantity ELSE 0 END) AS total_shares
    FROM date_ticker_combinations dt
    LEFT JOIN transactions t ON dt.ticker = t.ticker AND t.date <= dt.date
    GROUP BY dt.date, dt.ticker
),

stock_prices AS (
    SELECT
        date,
        ticker,
        close AS close_price
    FROM {{ source('stock_dataset', 'stock_data') }}
),

daily_values AS (
    SELECT
        dh.date,
        dh.ticker,
        dh.total_shares,
        sp.close_price,
        dh.total_shares * sp.close_price AS daily_value
    FROM daily_holdings dh
    JOIN stock_prices sp ON dh.date = sp.date AND dh.ticker = sp.ticker
    WHERE dh.total_shares > 0
)

SELECT
    date,
    ticker,
    total_shares,
    close_price,
    daily_value
FROM daily_values