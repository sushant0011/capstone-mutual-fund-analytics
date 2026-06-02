-- ========================================================
-- 10 ANALYTICAL SQL QUERIES FOR BLUESTOCK MUTUAL FUND ANALYTICS
-- ========================================================

-- 1. Top 5 Funds by Asset Under Management (AUM)
SELECT amfi_code, one_year_return, aum 
FROM fact_performance 
ORDER BY aum DESC 
LIMIT 5;

-- 2. Average NAV per Month (For each scheme)
SELECT amfi_code, strftime('%Y-%m', date) AS month, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- 3. Total Transaction Volume & Amount by Transaction Type (SIP/Lumpsum/Redemption YoY Check)
SELECT strftime('%Y', transaction_date) AS year, transaction_type, COUNT(*) AS total_transactions, SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY year, transaction_type
ORDER BY year, transaction_type;

-- 4. Geographical Transaction Distribution (Transactions by State)
SELECT state, COUNT(*) AS total_transactions, SUM(amount) AS total_invested_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_invested_amount DESC;

-- 5. Cost Efficient Schemes (Funds with expense_ratio < 1%)
SELECT f.amfi_code, f.scheme_name, p.expense_ratio, p.one_year_return
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- 6. High Performing Funds (Top 5 schemes based on 3-Year CAGR Return)
SELECT f.scheme_name, p.three_year_return, p.aum
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.three_year_return DESC
LIMIT 5;

-- 7. KYC Compliance Status Analysis across Investors
SELECT kyc_status, COUNT(DISTINCT investor_id) AS investor_count, COUNT(*) AS transaction_count
FROM fact_transactions
GROUP BY kyc_status;

-- 8. Scheme with Maximum NAV Volatility (Max NAV - Min NAV)
SELECT amfi_code, MAX(nav) AS peak_nav, MIN(nav) AS lowest_nav, (MAX(nav) - MIN(nav)) AS nav_spread
FROM fact_nav
GROUP BY amfi_code
ORDER BY nav_spread DESC
LIMIT 5;

-- 9. Top 5 States with Maximum SIP Registrations
SELECT state, COUNT(*) AS total_sip_count
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY total_sip_count DESC
LIMIT 5;

-- 10. Total Outflow (Redemptions) vs Inflow (SIP + Lumpsum)
SELECT 
    SUM(CASE WHEN transaction_type IN ('SIP', 'Lumpsum') THEN amount ELSE 0 END) AS total_inflow,
    SUM(CASE WHEN transaction_type = 'Redemption' THEN amount ELSE 0 END) AS total_outflow
FROM fact_transactions;