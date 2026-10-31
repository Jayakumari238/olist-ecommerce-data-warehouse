import sqlite3, pandas as pd

con = sqlite3.connect("olist.db")
q = lambda s: pd.read_sql(s, con).iloc[0, 0]

checks = {
    "fact rows > 0": q("SELECT COUNT(*) FROM fact_orders") > 0,
    "no null customer keys": q("SELECT COUNT(*) FROM fact_orders WHERE customer_id IS NULL") == 0,
    "no duplicate order items": q("""SELECT COUNT(*) FROM (SELECT order_id, order_item_id
        FROM fact_orders GROUP BY 1,2 HAVING COUNT(*)>1)""") == 0,
    "no orphan customers": q("""SELECT COUNT(*) FROM fact_orders f LEFT JOIN dim_customer c
        ON f.customer_id=c.customer_id WHERE c.customer_id IS NULL""") == 0,
    "no orphan products": q("""SELECT COUNT(*) FROM fact_orders f LEFT JOIN dim_product p
        ON f.product_id=p.product_id WHERE p.product_id IS NULL""") == 0,
    "no orphan sellers": q("""SELECT COUNT(*) FROM fact_orders f LEFT JOIN dim_seller s
        ON f.seller_id=s.seller_id WHERE s.seller_id IS NULL""") == 0,
    "no orphan dates": q("""SELECT COUNT(*) FROM fact_orders f LEFT JOIN dim_date d
        ON f.date_key=d.date_key WHERE d.date_key IS NULL""") == 0,
}
for name, ok in checks.items():
    print("PASS" if ok else "FAIL", "-", name)
