-- ==========================================
-- SALES ANALYSIS
-- ==========================================

USE sales_analysis;


-- 1. Total Revenue
SELECT
    SUM(revenue) AS total_revenue
FROM order_items;


-- 2. Total Profit
SELECT
    SUM(profit) AS total_profit
FROM order_items;


-- 3. Average Order Value
SELECT
    SUM(oi.revenue) / COUNT(DISTINCT o.order_id) AS average_order_value
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id;


-- 4. Top 10 Customers by Revenue
SELECT
    c.customer_id,
    c.customer_name,
    SUM(oi.revenue) AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Top 10 Products by Revenue
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.revenue) AS total_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 6. Products with Highest Profit
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.profit) AS total_profit
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_profit DESC
LIMIT 10;


-- 7. High Revenue but Low Profit Products
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.revenue) AS total_revenue,
    SUM(oi.profit) AS total_profit,
    SUM(oi.profit) / SUM(oi.revenue) AS profit_margin
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
HAVING SUM(oi.revenue) > 100000
   AND SUM(oi.profit) / SUM(oi.revenue) < 0.20
ORDER BY total_revenue DESC;


-- 8. Customers Who Stopped Purchasing
SELECT
    c.customer_id,
    c.customer_name,
    MAX(o.order_date) AS last_purchase_date
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING MAX(o.order_date) < DATE_SUB(
    (SELECT MAX(order_date) FROM orders),
    INTERVAL 90 DAY
)
ORDER BY last_purchase_date;


-- 9. Regions with Highest Revenue
SELECT
    c.region,
    SUM(oi.revenue) AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.region
ORDER BY total_revenue DESC;


-- 10. Underperforming Categories
SELECT
    p.category,
    SUM(oi.revenue) AS total_revenue,
    SUM(oi.profit) AS total_profit,
    SUM(oi.profit) / SUM(oi.revenue) AS profit_margin
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY profit_margin ASC;


-- 11. Month-over-Month Revenue Growth
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
    LAG(monthly_revenue) OVER (
        ORDER BY sales_month
    ) AS previous_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (
            ORDER BY sales_month
        ))
        / LAG(monthly_revenue) OVER (
            ORDER BY sales_month
        ) * 100,
        2
    ) AS growth_percentage
FROM monthly_revenue
ORDER BY sales_month;


-- 12. Customer Repeat-Purchase Rate
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT
    ROUND(
        SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)
        / COUNT(*) * 100,
        2
    ) AS repeat_purchase_rate
FROM customer_orders;