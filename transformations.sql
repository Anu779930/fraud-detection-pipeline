-- ============================================================
-- Fraud Detection Pipeline — SQL Transformations
-- Author: Venkata Sai Anusha Kommasani
-- Description: Data transformation and analysis queries
-- ============================================================


-- ── 1. Remove Duplicate Transactions ─────────────────────────────────────────
CREATE TABLE clean_transactions AS
SELECT DISTINCT *
FROM raw_transactions;


-- ── 2. Normalize Transaction Amounts ─────────────────────────────────────────
ALTER TABLE clean_transactions
ADD COLUMN Amount_Normalized FLOAT;

UPDATE clean_transactions
SET Amount_Normalized = (
    Amount - (SELECT AVG(Amount) FROM clean_transactions)
) / (SELECT STDDEV(Amount) FROM clean_transactions);


-- ── 3. Assign Risk Categories ─────────────────────────────────────────────────
ALTER TABLE clean_transactions
ADD COLUMN Risk_Category VARCHAR(20);

UPDATE clean_transactions
SET Risk_Category = CASE
    WHEN Amount > 1000 THEN 'High Risk'
    WHEN Amount > 500  THEN 'Medium Risk'
    WHEN Amount > 100  THEN 'Low Risk'
    ELSE 'Minimal Risk'
END;


-- ── 4. Summary Statistics by Fraud Label ──────────────────────────────────────
SELECT
    Class                        AS fraud_label,
    COUNT(*)                     AS transaction_count,
    ROUND(AVG(Amount), 2)        AS avg_amount,
    ROUND(MAX(Amount), 2)        AS max_amount,
    ROUND(MIN(Amount), 2)        AS min_amount,
    ROUND(STDDEV(Amount), 2)     AS std_amount
FROM clean_transactions
GROUP BY Class
ORDER BY Class;


-- ── 5. Fraud Rate by Risk Category ────────────────────────────────────────────
SELECT
    Risk_Category,
    COUNT(*)                                         AS total_transactions,
    SUM(Class)                                       AS fraud_count,
    ROUND(SUM(Class) * 100.0 / COUNT(*), 2)          AS fraud_rate_pct
FROM clean_transactions
GROUP BY Risk_Category
ORDER BY fraud_rate_pct DESC;


-- ── 6. High Value Fraud Transactions ─────────────────────────────────────────
SELECT *
FROM clean_transactions
WHERE Class = 1
  AND Amount > 500
ORDER BY Amount DESC
LIMIT 50;


-- ── 7. Transaction Volume Over Time ──────────────────────────────────────────
SELECT
    FLOOR(Time / 3600)   AS hour_of_day,
    COUNT(*)             AS total_transactions,
    SUM(Class)           AS fraud_count,
    ROUND(AVG(Amount),2) AS avg_amount
FROM clean_transactions
GROUP BY hour_of_day
ORDER BY hour_of_day;


-- ── 8. Data Quality Check Query ──────────────────────────────────────────────
SELECT
    COUNT(*)                                 AS total_records,
    SUM(CASE WHEN Amount IS NULL THEN 1 END) AS null_amounts,
    SUM(CASE WHEN Class IS NULL  THEN 1 END) AS null_class,
    SUM(CASE WHEN Amount < 0     THEN 1 END) AS negative_amounts,
    SUM(CASE WHEN Class NOT IN (0,1) THEN 1 END) AS invalid_class_values
FROM clean_transactions;


-- ── 9. KPI Summary for Power BI Dashboard ────────────────────────────────────
SELECT
    COUNT(*)                                         AS total_transactions,
    SUM(Class)                                       AS total_fraud,
    ROUND(SUM(Class) * 100.0 / COUNT(*), 4)          AS fraud_rate_pct,
    ROUND(SUM(CASE WHEN Class=1 THEN Amount END), 2) AS total_fraud_amount,
    ROUND(AVG(Amount), 2)                            AS avg_transaction_amount,
    COUNT(DISTINCT Risk_Category)                    AS risk_categories
FROM clean_transactions;
