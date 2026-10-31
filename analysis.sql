-- 1. Monthly revenue + growth %
WITH m AS (
  SELECT d.year, d.month, ROUND(SUM(f.price),0) AS revenue
  FROM fact_orders f JOIN dim_date d ON f.date_key = d.date_key
  GROUP BY d.year, d.month)
SELECT *, ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year, month))
       / LAG(revenue) OVER (ORDER BY year, month), 1) AS growth_pct
FROM m;

-- 2. Top 10 sellers by revenue
SELECT seller_id, ROUND(SUM(price),0) AS revenue,
       RANK() OVER (ORDER BY SUM(price) DESC) AS rnk
FROM fact_orders GROUP BY seller_id ORDER BY rnk LIMIT 10;

-- 3. Late delivery % by state
SELECT customer_state, COUNT(*) AS orders,
       ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS late_pct
FROM (SELECT DISTINCT f.order_id, c.customer_state, f.is_late
      FROM fact_orders f JOIN dim_customer c ON f.customer_id = c.customer_id)
GROUP BY customer_state ORDER BY late_pct DESC;

-- 4. Late delivery vs review score
SELECT is_late, COUNT(*) AS orders, ROUND(AVG(review_score),2) AS avg_review
FROM (SELECT DISTINCT order_id, is_late, review_score FROM fact_orders)
GROUP BY is_late;

-- 5. Repeat customer %
WITH cust AS (
  SELECT c.customer_unique_id, COUNT(DISTINCT f.order_id) AS n
  FROM fact_orders f JOIN dim_customer c ON f.customer_id = c.customer_id
  GROUP BY 1)
SELECT ROUND(100.0 * SUM(n > 1) / COUNT(*), 2) AS repeat_pct FROM cust;
