-- ==========================================
-- CLEANING & DATA QUALITY CHECKS
-- ==========================================

-- 1. Check Duplicate Customers
SELECT customer_id, COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- 2. Check Invalid Product Prices
SELECT *
FROM products
WHERE cost_price <= 0
   OR list_price <= 0;


-- 3. Validate Orders and Customers Relationship
SELECT o.customer_id
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- 4. Check Invalid Order Item Values
SELECT *
FROM order_items
WHERE quantity <= 0
   OR discount < 0
   OR discount > 1;


-- 5. Validate Order Items and Products Relationship
SELECT oi.product_id
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- 6. Basic Filtering and Sorting - Highest Revenue
SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    revenue,
    profit
FROM order_items
ORDER BY revenue DESC;


-- 7. Calculate Total Revenue
SELECT SUM(revenue) AS total_revenue
FROM order_items;


-- 8. Calculate Total Profit
SELECT SUM(profit) AS total_profit
FROM order_items;