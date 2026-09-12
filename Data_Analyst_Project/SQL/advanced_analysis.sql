-- ==========================================
-- ADVANCED SALES ANALYSIS
-- ==========================================

USE sales_analysis;


-- 1. Customer Revenue using CTE
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.revenue) AS total_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.customer_id
)
SELECT
    customer_id,
    total_revenue
FROM customer_revenue
ORDER BY total_revenue DESC;


-- 2. Customer Revenue Segmentation using CASE
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.revenue) AS total_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.customer_id
)
SELECT
    customer_id,
    total_revenue,
    CASE
        WHEN total_revenue >= 200000 THEN 'High Value'
        WHEN total_revenue >= 100000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM customer_revenue
ORDER BY total_revenue DESC;


-- 3. Customer Revenue Ranking
SELECT
    c.customer_id,
    c.customer_name,
    SUM(oi.revenue) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(oi.revenue) DESC
    ) AS revenue_rank
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY revenue_rank;


-- 4. Monthly Revenue Running Total
WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
        SUM(oi.revenue) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT
    sales_month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (
        ORDER BY sales_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM monthly_revenue
ORDER BY sales_month;


-- 5. Product Profit Margin Ranking
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.revenue) AS total_revenue,
    SUM(oi.profit) AS total_profit,
    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin_percentage,
    RANK() OVER (
        ORDER BY SUM(oi.profit) DESC
    ) AS profit_rank
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY profit_rank;


-- 6. Customer Monthly Revenue and Running Total
WITH customer_monthly_revenue AS (
    SELECT
        o.customer_id,
        DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
        SUM(oi.revenue) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.customer_id,
        DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT
    customer_id,
    sales_month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (
        PARTITION BY customer_id
        ORDER BY sales_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS customer_running_revenue
FROM customer_monthly_revenue
ORDER BY customer_id, sales_month;


-- 7. Category Performance Ranking
SELECT
    p.category,
    SUM(oi.revenue) AS total_revenue,
    SUM(oi.profit) AS total_profit,
    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin_percentage,
    RANK() OVER (
        ORDER BY SUM(oi.profit) DESC
    ) AS profit_rank
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY profit_rank;