import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

customers = pd.read_csv("customers_cleaned.csv")
products = pd.read_csv("products_cleaned.csv")
orders = pd.read_csv("orders_cleaned.csv")
order_items = pd.read_csv("order_items_cleaned.csv")
payments = pd.read_csv("payments_cleaned.csv")
returns = pd.read_csv("returns_cleaned.csv")
marketing = pd.read_csv("marketing_cleaned.csv")

# ==========================================
# STEP 1 - EXPLORATORY DATA ANALYSIS
# ==========================================

print("CUSTOMERS")
print(customers.shape)
print(customers.info())
print(customers.isnull().sum())
print("Duplicates:", customers.duplicated().sum())

print("\nPRODUCTS")
print(products.shape)
print(products.info())
print(products.isnull().sum())
print("Duplicates:", products.duplicated().sum())

print("\nORDERS")
print(orders.shape)
print(orders.info())
print(orders.isnull().sum())
print("Duplicates:", orders.duplicated().sum())

print("\nORDER ITEMS")
print(order_items.shape)
print(order_items.info())
print(order_items.isnull().sum())
print("Duplicates:", order_items.duplicated().sum())

print("\nPAYMENTS")
print(payments.shape)
print(payments.info())
print(payments.isnull().sum())
print("Duplicates:", payments.duplicated().sum())

print("\nRETURNS")
print(returns.shape)
print(returns.info())
print(returns.isnull().sum())
print("Duplicates:", returns.duplicated().sum())

print("\nMARKETING")
print(marketing.shape)
print(marketing.info())
print(marketing.isnull().sum())
print("Duplicates:", marketing.duplicated().sum())

# ==========================================
# CHART 1 - MONTHLY SALES TREND
# ==========================================

orders['order_date'] = pd.to_datetime(orders['order_date'])

monthly_sales = (
    orders.merge(
        order_items[['order_id', 'revenue']],
        on='order_id',
        how='inner'
    )
    .groupby(orders['order_date'].dt.to_period('M'))['revenue']
    .sum()
)

plt.figure(figsize=(12, 6))
plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker='o'
)

plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================
# CHART 2 - MONTHLY PROFIT TREND
# ==========================================

profit_data = orders.merge(
    order_items[['order_id', 'profit']],
    on='order_id',
    how='inner'
)

profit_data['order_date'] = pd.to_datetime(
    profit_data['order_date']
)

profit_data['sales_month'] = (
    profit_data['order_date']
    .dt.to_period('M')
)

monthly_profit = (
    profit_data
    .groupby('sales_month')['profit']
    .sum()
)

plt.figure(figsize=(12, 6))
plt.plot(
    monthly_profit.index.astype(str),
    monthly_profit.values,
    marker='o'
)

plt.title('Monthly Profit Trend')
plt.xlabel('Month')
plt.ylabel('Profit')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================
# CHART 3 - TOP 10 PRODUCTS BY REVENUE
# ==========================================

product_sales = (
    order_items
    .groupby('product_id')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

product_names = products.set_index('product_id')['product_name']

product_sales.index = product_sales.index.map(product_names)

plt.figure(figsize=(12, 6))
plt.bar(product_sales.index, product_sales.values)

plt.title('Top 10 Products by Revenue')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ==========================================
# CHART 4 - REVENUE BY REGION
# ==========================================

region_sales = (
    orders
    .merge(
        customers[['customer_id', 'region']],
        on='customer_id',
        how='left'
    )
    .merge(
        order_items[['order_id', 'revenue']],
        on='order_id',
        how='inner'
    )
    .groupby('region')['revenue']
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
plt.bar(region_sales.index, region_sales.values)

plt.title('Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================
# CHART 5 - CUSTOMER REVENUE DISTRIBUTION
# ==========================================

customer_sales = (
    orders
    .merge(
        order_items[['order_id', 'revenue']],
        on='order_id',
        how='inner'
    )
    .groupby('customer_id')['revenue']
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))
plt.hist(customer_sales.values, bins=20)

plt.title('Customer Revenue Distribution')
plt.xlabel('Total Revenue per Customer')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.show()

# ==========================================
# CHART 6 - RETURNS BY REASON
# ==========================================

return_reasons = (
    returns['return_reason']
    .value_counts()
)

plt.figure(figsize=(10, 6))
plt.bar(
    return_reasons.index,
    return_reasons.values
)

plt.title('Returns by Reason')
plt.xlabel('Return Reason')
plt.ylabel('Number of Returns')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ==========================================
# CHART 7 - MARKETING CHANNEL PERFORMANCE
# ==========================================

channel_revenue = (
    marketing
    .groupby('channel')['revenue_generated']
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
plt.bar(
    channel_revenue.index,
    channel_revenue.values
)

plt.title('Revenue Generated by Marketing Channel')
plt.xlabel('Marketing Channel')
plt.ylabel('Revenue Generated')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ==========================================
# CHART 8 - MARKETING ROI BY CHANNEL
# ==========================================

channel_roi = (
    marketing
    .groupby('channel')['roi']
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
plt.bar(
    channel_roi.index,
    channel_roi.values
)

plt.title('Average Marketing ROI by Channel')
plt.xlabel('Marketing Channel')
plt.ylabel('Average ROI')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ==========================================
# CHART 9 - REVENUE OUTLIER DETECTION
# ==========================================

plt.figure(figsize=(10, 6))

plt.boxplot(
    order_items['revenue'].dropna()
)

plt.title('Order Item Revenue - Outlier Detection')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()

# ==========================================
# CHART 10 - CORRELATION HEATMAP
# ==========================================

numeric_data = order_items[
    [
        'quantity',
        'unit_price',
        'discount',
        'cost_price',
        'gross_sales',
        'discount_amount',
        'revenue',
        'cost',
        'profit',
        'profit_margin'
    ]
]

correlation_matrix = numeric_data.corr()

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    linewidths=0.5
)

plt.title('Correlation Heatmap - Order Items')
plt.tight_layout()
plt.show()

# ==========================================
# PART 4 - STATISTICAL ANALYSIS
# STEP 1 - MEAN, MEDIAN & STANDARD DEVIATION
# ==========================================

revenue = order_items['revenue'].dropna()

print("\nSTATISTICAL SUMMARY - REVENUE")
print("Mean Revenue:", revenue.mean())
print("Median Revenue:", revenue.median())
print("Standard Deviation:", revenue.std())

print("\nSTATISTICAL SUMMARY - PROFIT")
profit = order_items['profit'].dropna()

print("Mean Profit:", profit.mean())
print("Median Profit:", profit.median())
print("Standard Deviation:", profit.std())

# ==========================================
# PART 4 - STATISTICAL ANALYSIS
# STEP 2 - CORRELATION ANALYSIS
# ==========================================

correlation_data = order_items[
    [
        'quantity',
        'unit_price',
        'discount',
        'cost_price',
        'revenue',
        'cost',
        'profit',
        'profit_margin'
    ]
].dropna()

correlation_matrix = correlation_data.corr()

print("\nCORRELATION MATRIX")
print(correlation_matrix.round(3))

# ==========================================
# STEP 3 - 95% CONFIDENCE INTERVAL
# ==========================================

from scipy import stats

revenue = order_items['revenue'].dropna()

sample_mean = revenue.mean()
sample_std = revenue.std()
sample_size = len(revenue)

confidence_level = 0.95
standard_error = sample_std / np.sqrt(sample_size)

margin_of_error = stats.t.ppf(
    (1 + confidence_level) / 2,
    sample_size - 1
) * standard_error

lower_bound = sample_mean - margin_of_error
upper_bound = sample_mean + margin_of_error

print("\n95% CONFIDENCE INTERVAL - REVENUE")
print("Mean Revenue:", round(sample_mean, 2))
print("Lower Bound:", round(lower_bound, 2))
print("Upper Bound:", round(upper_bound, 2))



# ==========================================
# STEP 4 - NEW CAMPAIGN IDENTIFICATION
# ==========================================

print("\nMARKETING CAMPAIGNS")
print(
    marketing[
        [
            'campaign_id',
            'campaign_name',
            'channel',
            'start_date',
            'impressions',
            'clicks',
            'conversions',
            'conversion_rate'
        ]
    ].to_string(index=False)
)

# ==========================================
# STEP 4 - HYPOTHESIS TESTING
# NEW CAMPAIGN vs PREVIOUS CAMPAIGN
# ==========================================

previous_campaign = marketing.iloc[-2]
new_campaign = marketing.iloc[-1]

x1 = int(new_campaign['conversions'])
n1 = int(new_campaign['impressions'])

x2 = int(previous_campaign['conversions'])
n2 = int(previous_campaign['impressions'])

p1 = x1 / n1
p2 = x2 / n2

# Pooled proportion
pooled_p = (x1 + x2) / (n1 + n2)

# Standard error
standard_error = np.sqrt(
    pooled_p * (1 - pooled_p) * (1/n1 + 1/n2)
)

# Z statistic
z_stat = (p1 - p2) / standard_error

# One-tailed p-value
p_value = 1 - (0.5 * (1 + math.erf(z_stat / np.sqrt(2))))
alpha = 0.05

print("\nHYPOTHESIS TEST - CONVERSION RATE")
print("Previous Campaign:", previous_campaign['campaign_name'])
print("Previous Conversion Rate:", round(p2, 4))

print("New Campaign:", new_campaign['campaign_name'])
print("New Conversion Rate:", round(p1, 4))

print("Significance Level:", alpha)
print("Z-statistic:", round(z_stat, 4))
print("P-value:", round(p_value, 6))

if p_value < alpha:
    print("Result: Reject the Null Hypothesis")
    print("Conclusion: The new campaign produced a statistically significant improvement in conversion rate.")
else:
    print("Result: Fail to Reject the Null Hypothesis")
    print("Conclusion: There is not enough evidence to conclude that the new campaign significantly improved conversion rate.")

# ==========================================
# PART 5 - CUSTOMER ANALYSIS
# STEP 1 - CUSTOMER PURCHASING BEHAVIOR
# ==========================================

customer_data = (
    orders
    .merge(
        order_items[['order_id', 'revenue']],
        on='order_id',
        how='inner'
    )
)

customer_summary = (
    customer_data
    .groupby('customer_id')
    .agg(
        total_spending=('revenue', 'sum'),
        number_of_orders=('order_id', 'nunique')
    )
)

customer_summary['average_order_value'] = (
    customer_summary['total_spending'] /
    customer_summary['number_of_orders']
)

print("\nCUSTOMER PURCHASING BEHAVIOR")
print(customer_summary.head(10))

# ==========================================
# PART 5 - CUSTOMER ANALYSIS
# STEP 2 - PURCHASE FREQUENCY & RECENCY
# ==========================================

orders['order_date'] = pd.to_datetime(orders['order_date'])

customer_frequency = (
    orders
    .groupby('customer_id')
    .agg(
        purchase_frequency=('order_id', 'nunique'),
        last_purchase_date=('order_date', 'max')
    )
)

analysis_date = orders['order_date'].max()

customer_frequency['recency_days'] = (
    analysis_date - customer_frequency['last_purchase_date']
).dt.days

print("\nCUSTOMER PURCHASE FREQUENCY & RECENCY")
print(customer_frequency.head(10))

# ==========================================
# PART 5 - CUSTOMER ANALYSIS
# STEP 3 - CUSTOMER LIFETIME VALUE
# ==========================================

customer_summary['purchase_frequency'] = (
    customer_frequency['purchase_frequency']
)

customer_summary['recency_days'] = (
    customer_frequency['recency_days']
)

customer_summary['customer_lifetime_value'] = (
    customer_summary['average_order_value']
    * customer_summary['purchase_frequency']
)

print("\nCUSTOMER LIFETIME VALUE")
print(
    customer_summary[
        [
            'total_spending',
            'number_of_orders',
            'average_order_value',
            'purchase_frequency',
            'recency_days',
            'customer_lifetime_value'
        ]
    ].head(10)
)

# ==========================================
# PART 5 - CUSTOMER ANALYSIS
# STEP 4 - CUSTOMER SEGMENTATION
# ==========================================

# Create customer analysis table
customer_analysis = customer_summary.copy()

# Customer segmentation rules
def customer_segment(row):

    spending = row['total_spending']
    frequency = row['purchase_frequency']
    recency = row['recency_days']

    # Inactive: no recent purchase
    if recency > 365:
        return 'Inactive Customers'

    # At-Risk: purchased before, but not recently
    elif recency > 180:
        return 'At-Risk Customers'

    # VIP: high spending and frequent purchases
    elif spending >= 150000 and frequency >= 5:
        return 'VIP Customers'

    # High-Value: strong spending
    elif spending >= 75000:
        return 'High-Value Customers'

    # Regular: moderate spending and activity
    elif spending >= 30000 and frequency >= 2:
        return 'Regular Customers'

    # Low-Value: lower spending
    else:
        return 'Low-Value Customers'


customer_analysis['segment'] = (
    customer_analysis.apply(customer_segment, axis=1)
)

print("\nCUSTOMER SEGMENTATION")
print(
    customer_analysis[
        [
            'total_spending',
            'number_of_orders',
            'average_order_value',
            'purchase_frequency',
            'recency_days',
            'customer_lifetime_value',
            'segment'
        ]
    ].head(20)
)


# ==========================================
# STEP 5 - SEGMENT SUMMARY
# ==========================================

segment_summary = (
    customer_analysis
    .groupby('segment')
    .agg(
        customers=('segment', 'count'),
        total_spending=('total_spending', 'sum'),
        average_spending=('total_spending', 'mean'),
        average_orders=('number_of_orders', 'mean'),
        average_order_value=('average_order_value', 'mean'),
        average_recency=('recency_days', 'mean'),
        average_clv=('customer_lifetime_value', 'mean')
    )
    .sort_values('total_spending', ascending=False)
)

print("\nCUSTOMER SEGMENT SUMMARY")
print(segment_summary.round(2))


# ==========================================
# STEP 6 - SEGMENT DISTRIBUTION
# ==========================================

segment_counts = customer_analysis['segment'].value_counts()

print("\nCUSTOMER SEGMENT DISTRIBUTION")
print(segment_counts)


# ==========================================
# STEP 7 - CUSTOMER SEGMENT CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    segment_counts.index,
    segment_counts.values
)

plt.title('Customer Segment Distribution')
plt.xlabel('Customer Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()


# ==========================================
# PART 6 - PRODUCT ANALYSIS
# COMPLETE PRODUCT PERFORMANCE ANALYSIS
# ==========================================

# Create product-level analysis
product_analysis = (
    order_items
    .groupby('product_id')
    .agg(
        total_quantity=('quantity', 'sum'),
        total_revenue=('revenue', 'sum'),
        total_profit=('profit', 'sum'),
        average_discount=('discount', 'mean')
    )
)

# Calculate profit margin
product_analysis['profit_margin'] = np.where(
    product_analysis['total_revenue'] != 0,
    (product_analysis['total_profit'] /
     product_analysis['total_revenue']) * 100,
    0
)

# Add product details
product_analysis = product_analysis.reset_index()

product_analysis = product_analysis.merge(
    products[
        ['product_id', 'product_name', 'category']
    ],
    on='product_id',
    how='left'
)


# ==========================================
# 1. TOP-SELLING PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("TOP 10 BEST-SELLING PRODUCTS")
print("=" * 60)

top_selling = (
    product_analysis
    .sort_values('total_quantity', ascending=False)
    .head(10)
)

print(
    top_selling[
        [
            'product_name',
            'category',
            'total_quantity',
            'total_revenue'
        ]
    ].to_string(index=False)
)


# ==========================================
# 2. MOST PROFITABLE PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("TOP 10 MOST PROFITABLE PRODUCTS")
print("=" * 60)

most_profitable = (
    product_analysis
    .sort_values('total_profit', ascending=False)
    .head(10)
)

print(
    most_profitable[
        [
            'product_name',
            'category',
            'total_profit',
            'profit_margin'
        ]
    ].to_string(index=False)
)


# ==========================================
# 3. LOW-PERFORMING PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("TOP 10 LOW-PERFORMING PRODUCTS")
print("=" * 60)

low_performing = (
    product_analysis
    .sort_values('total_revenue', ascending=True)
    .head(10)
)

print(
    low_performing[
        [
            'product_name',
            'category',
            'total_quantity',
            'total_revenue',
            'total_profit'
        ]
    ].to_string(index=False)
)


# ==========================================
# 4. LOSS-MAKING PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("LOSS-MAKING PRODUCTS")
print("=" * 60)

loss_making = (
    product_analysis[
        product_analysis['total_profit'] < 0
    ]
    .sort_values('total_profit')
)

if len(loss_making) > 0:
    print(
        loss_making[
            [
                'product_name',
                'category',
                'total_revenue',
                'total_profit',
                'profit_margin'
            ]
        ].to_string(index=False)
    )
else:
    print("No loss-making products found.")


# ==========================================
# 5. HIGH-RETURN PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("HIGH-RETURN PRODUCTS")
print("=" * 60)

return_data = (
    returns
    .groupby('product_id')
    .agg(
        return_count=('return_id', 'count'),
        total_refund=('refund_amount', 'sum')
    )
    .reset_index()
)

return_data = return_data.merge(
    products[
        ['product_id', 'product_name', 'category']
    ],
    on='product_id',
    how='left'
)

high_return_products = (
    return_data
    .sort_values('return_count', ascending=False)
    .head(10)
)

print(
    high_return_products[
        [
            'product_name',
            'category',
            'return_count',
            'total_refund'
        ]
    ].to_string(index=False)
)


# ==========================================
# 6. HIGH-DISCOUNT PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("TOP 10 HIGH-DISCOUNT PRODUCTS")
print("=" * 60)

high_discount = (
    product_analysis
    .sort_values('average_discount', ascending=False)
    .head(10)
)

print(
    high_discount[
        [
            'product_name',
            'category',
            'average_discount',
            'total_revenue',
            'total_profit'
        ]
    ].to_string(index=False)
)


# ==========================================
# 7. HIGH-REVENUE BUT LOW-MARGIN PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("HIGH-REVENUE BUT LOW-MARGIN PRODUCTS")
print("=" * 60)

revenue_threshold = (
    product_analysis['total_revenue'].quantile(0.75)
)

margin_threshold = (
    product_analysis['profit_margin'].quantile(0.25)
)

high_revenue_low_margin = product_analysis[
    (product_analysis['total_revenue'] >= revenue_threshold) &
    (product_analysis['profit_margin'] <= margin_threshold)
].sort_values(
    'total_revenue',
    ascending=False
)

if len(high_revenue_low_margin) > 0:
    print(
        high_revenue_low_margin[
            [
                'product_name',
                'category',
                'total_revenue',
                'total_profit',
                'profit_margin'
            ]
        ].to_string(index=False)
    )
else:
    print("No high-revenue low-margin products found.")


# ==========================================
# 8. PRODUCT MANAGEMENT RECOMMENDATIONS
# ==========================================

print("\n" + "=" * 60)
print("PRODUCT MANAGEMENT RECOMMENDATIONS")
print("=" * 60)

print("""
1. Focus on top-selling products to maintain stock availability.

2. Promote highly profitable products because they contribute
   strongly to overall profitability.

3. Review low-performing products for pricing, demand,
   positioning, or inventory decisions.

4. Investigate loss-making products and consider price,
   cost, discount, or supplier optimization.

5. Investigate high-return products to identify product quality,
   description, delivery, or customer-expectation issues.

6. Review high-discount products because excessive discounting
   can reduce profitability.

7. Monitor high-revenue but low-margin products because they
   generate sales but may contribute relatively less profit.
""")


# ==========================================
# 9. PRODUCT PERFORMANCE CHART
# ==========================================

plt.figure(figsize=(12, 6))

plt.bar(
    top_selling['product_name'],
    top_selling['total_quantity']
)

plt.title('Top 10 Best-Selling Products')
plt.xlabel('Product')
plt.ylabel('Quantity Sold')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()


# ==========================================
# 10. PROFITABLE PRODUCTS CHART
# ==========================================

plt.figure(figsize=(12, 6))

plt.bar(
    most_profitable['product_name'],
    most_profitable['total_profit']
)

plt.title('Top 10 Most Profitable Products')
plt.xlabel('Product')
plt.ylabel('Profit')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# ==========================================
# PART 7 - MARKETING ANALYSIS
# COMPLETE MARKETING PERFORMANCE ANALYSIS
# ==========================================

# ==========================================
# 1. CAMPAIGN PERFORMANCE
# ==========================================

print("\n" + "=" * 60)
print("MARKETING CAMPAIGN PERFORMANCE")
print("=" * 60)

marketing_analysis = marketing.copy()

print(
    marketing_analysis[
        [
            'campaign_name',
            'channel',
            'impressions',
            'clicks',
            'conversions',
            'conversion_rate',
            'cac',
            'revenue_generated',
            'roi'
        ]
    ].to_string(index=False)
)


# ==========================================
# 2. MARKETING CHANNEL ANALYSIS
# ==========================================

channel_analysis = (
    marketing
    .groupby('channel')
    .agg(
        impressions=('impressions', 'sum'),
        clicks=('clicks', 'sum'),
        conversions=('conversions', 'sum'),
        spend=('spend', 'sum'),
        revenue_generated=('revenue_generated', 'sum')
    )
)

# Calculate CTR
channel_analysis['ctr'] = (
    channel_analysis['clicks'] /
    channel_analysis['impressions'] * 100
)

# Calculate Conversion Rate
channel_analysis['conversion_rate'] = (
    channel_analysis['conversions'] /
    channel_analysis['clicks'] * 100
)

# Calculate CAC
channel_analysis['cac'] = (
    channel_analysis['spend'] /
    channel_analysis['conversions']
)

# Calculate ROI
channel_analysis['roi'] = (
    (channel_analysis['revenue_generated'] -
     channel_analysis['spend']) /
    channel_analysis['spend'] * 100
)

print("\n" + "=" * 60)
print("MARKETING CHANNEL PERFORMANCE")
print("=" * 60)

print(
    channel_analysis
    .sort_values('roi', ascending=False)
    .round(2)
    .to_string()
)


# ==========================================
# 3. BEST ROI MARKETING CHANNEL
# ==========================================

best_channel = (
    channel_analysis['roi']
    .idxmax()
)

best_roi = (
    channel_analysis['roi']
    .max()
)

print("\n" + "=" * 60)
print("BEST MARKETING CHANNEL BY ROI")
print("=" * 60)

print("Best Channel:", best_channel)
print("ROI:", round(best_roi, 2), "%")


# ==========================================
# 4. BEST CHANNEL BY CONVERSION RATE
# ==========================================

best_conversion_channel = (
    channel_analysis['conversion_rate']
    .idxmax()
)

best_conversion_rate = (
    channel_analysis['conversion_rate']
    .max()
)

print("\n" + "=" * 60)
print("BEST CHANNEL BY CONVERSION RATE")
print("=" * 60)

print("Best Channel:", best_conversion_channel)
print(
    "Conversion Rate:",
    round(best_conversion_rate, 2),
    "%"
)


# ==========================================
# 5. LOWEST CUSTOMER ACQUISITION COST
# ==========================================

lowest_cac_channel = (
    channel_analysis['cac']
    .idxmin()
)

lowest_cac = (
    channel_analysis['cac']
    .min()
)

print("\n" + "=" * 60)
print("LOWEST CUSTOMER ACQUISITION COST")
print("=" * 60)

print("Channel:", lowest_cac_channel)
print("CAC:", round(lowest_cac, 2))


# ==========================================
# 6. HIGHEST REVENUE CHANNEL
# ==========================================

highest_revenue_channel = (
    channel_analysis['revenue_generated']
    .idxmax()
)

highest_revenue = (
    channel_analysis['revenue_generated']
    .max()
)

print("\n" + "=" * 60)
print("HIGHEST REVENUE MARKETING CHANNEL")
print("=" * 60)

print("Channel:", highest_revenue_channel)
print("Revenue:", round(highest_revenue, 2))


# ==========================================
# 7. MARKETING CHANNEL ROI CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    channel_analysis.index,
    channel_analysis['roi']
)

plt.title('Marketing ROI by Channel')
plt.xlabel('Marketing Channel')
plt.ylabel('ROI (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# 8. REVENUE BY MARKETING CHANNEL
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    channel_analysis.index,
    channel_analysis['revenue_generated']
)

plt.title('Revenue Generated by Marketing Channel')
plt.xlabel('Marketing Channel')
plt.ylabel('Revenue')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# 9. CONVERSION RATE BY CHANNEL
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    channel_analysis.index,
    channel_analysis['conversion_rate']
)

plt.title('Conversion Rate by Marketing Channel')
plt.xlabel('Marketing Channel')
plt.ylabel('Conversion Rate (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# 10. MARKETING RECOMMENDATIONS
# ==========================================

print("\n" + "=" * 60)
print("MARKETING MANAGEMENT RECOMMENDATIONS")
print("=" * 60)

print("""
1. Prioritize the marketing channel with the highest ROI.

2. Monitor channels with high customer acquisition costs.

3. Increase investment in channels that generate strong
   revenue and conversion rates.

4. Review low-performing channels and optimize campaign
   targeting and spending.

5. Use conversion rate together with ROI when evaluating
   campaign effectiveness.

6. Continuously monitor campaign performance to improve
   marketing budget allocation.
""")

# Save customer segment distribution for Power BI
segment_counts_df = (
    customer_analysis['segment']
    .value_counts()
    .rename_axis('segment')
    .reset_index(name='customers')
)

segment_counts_df.to_csv(
    "customer_segment_distribution.csv",
    index=False
)

print("Customer segment distribution saved successfully.")

customer_analysis.to_csv(
    "customer_analysis.csv",
    index=True
)

print("Customer analysis saved successfully.")