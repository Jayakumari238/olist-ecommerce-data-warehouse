import pandas as pd, sqlite3, os

RAW = "data/raw/"
os.makedirs("data/processed", exist_ok=True)
date_cols = ["order_purchase_timestamp", "order_approved_at",
             "order_delivered_carrier_date", "order_delivered_customer_date",
             "order_estimated_delivery_date"]

# ---------- EXTRACT ----------
orders = pd.read_csv(RAW + "olist_orders_dataset.csv", parse_dates=date_cols)
items = pd.read_csv(RAW + "olist_order_items_dataset.csv")
customers = pd.read_csv(RAW + "olist_customers_dataset.csv")
products = pd.read_csv(RAW + "olist_products_dataset.csv")
sellers = pd.read_csv(RAW + "olist_sellers_dataset.csv")
reviews = pd.read_csv(RAW + "olist_order_reviews_dataset.csv")
trans = pd.read_csv(RAW + "product_category_name_translation.csv")

# ---------- TRANSFORM ----------
orders = orders[orders.order_status == "delivered"].dropna(
    subset=["order_delivered_customer_date"]).copy()
orders["delivery_days"] = (orders.order_delivered_customer_date - orders.order_purchase_timestamp).dt.days
orders["delay_days"] = (orders.order_delivered_customer_date - orders.order_estimated_delivery_date).dt.days
orders["is_late"] = (orders.delay_days > 0).astype(int)
orders["date_key"] = orders.order_purchase_timestamp.dt.strftime("%Y%m%d").astype(int)

products = products.merge(trans, on="product_category_name", how="left")
products["category"] = products.product_category_name_english.fillna("unknown")

dim_product = products[["product_id", "category"]].drop_duplicates()
dim_customer = customers[["customer_id", "customer_unique_id",
                          "customer_city", "customer_state"]].drop_duplicates()
dim_seller = sellers[["seller_id", "seller_city", "seller_state"]].drop_duplicates()

dates = pd.date_range(orders.order_purchase_timestamp.min().normalize(),
                      orders.order_purchase_timestamp.max().normalize())
dim_date = pd.DataFrame({"date": dates})
dim_date["date_key"] = dim_date.date.dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date.date.dt.year
dim_date["month"] = dim_date.date.dt.month
dim_date["month_name"] = dim_date.date.dt.month_name()
dim_date["quarter"] = dim_date.date.dt.quarter
dim_date["day_of_week"] = dim_date.date.dt.day_name()
dim_date["date"] = dim_date.date.dt.strftime("%Y-%m-%d")

review_avg = reviews.groupby("order_id").review_score.mean().reset_index()

fact_orders = (items
    .merge(orders[["order_id", "customer_id", "date_key",
                   "delivery_days", "delay_days", "is_late"]], on="order_id")
    .merge(review_avg, on="order_id", how="left"))
fact_orders = fact_orders[["order_id", "order_item_id", "customer_id", "product_id",
                           "seller_id", "date_key", "price", "freight_value",
                           "review_score", "delivery_days", "delay_days", "is_late"]]

# ---------- LOAD ----------
tables = {"fact_orders": fact_orders, "dim_customer": dim_customer,
          "dim_product": dim_product, "dim_seller": dim_seller, "dim_date": dim_date}
con = sqlite3.connect("olist.db")
for name, df in tables.items():
    df.to_sql(name, con, if_exists="replace", index=False)
    df.to_csv(f"data/processed/{name}.csv", index=False)  # for Power BI
    print(f"{name}: {len(df)} rows loaded")
con.close()
print("ETL done")
