-- ==========================================
-- E-COMMERCE ANALYTICS DATABASE SCHEMA
-- ==========================================

CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;


-- 1. CUSTOMERS
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(150),
    region VARCHAR(50),
    city VARCHAR(80),
    signup_date DATE
);


-- 2. PRODUCTS
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(80),
    cost_price DECIMAL(12,2),
    list_price DECIMAL(12,2),
    stock_qty INT
);


-- 3. ORDERS
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    order_date DATE,
    order_status VARCHAR(30),
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- 4. ORDER ITEMS
CREATE TABLE order_items (
    order_item_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INT,
    unit_price DECIMAL(12,2),
    discount DECIMAL(5,2),
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- 5. PAYMENTS
CREATE TABLE payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20),
    payment_date DATE,
    payment_method VARCHAR(40),
    payment_amount DECIMAL(12,2),
    payment_status VARCHAR(30)
);


-- 6. RETURNS
CREATE TABLE returns (
    return_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20),
    product_id VARCHAR(20),
    return_date DATE,
    return_reason VARCHAR(80),
    refund_amount DECIMAL(12,2)
);


-- 7. MARKETING
CREATE TABLE marketing (
    campaign_id VARCHAR(20) PRIMARY KEY,
    campaign_name VARCHAR(100),
    channel VARCHAR(50),
    campaign_type VARCHAR(20),
    start_date DATE,
    impressions BIGINT,
    clicks BIGINT,
    conversions BIGINT,
    spend DECIMAL(14,2),
    revenue_generated DECIMAL(14,2)
);