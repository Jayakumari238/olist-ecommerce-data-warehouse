Olist E-Commerce Data Warehouse and Analytics

End-to-end data project on the Olist Brazilian e-commerce dataset: a Python ETL pipeline, a star-schema warehouse in SQLite, SQL analysis, and a Power BI dashboard.

Tech stack: Python (pandas), SQL (SQLite), Power BI (DAX)

Business questions
How has revenue grown, and when did it peak?
How often are deliveries late, and where?
Do late deliveries affect customer reviews?
Who are the top sellers, and how many customers come back?
Architecture
9 raw CSV files -> Python ETL (pandas) -> SQLite star schema -> SQL analysis -> Power BI dashboard
Star schema
Fact table: fact_orders (one row per order item: price, freight, review score, delivery days, delay days, late flag)
Dimensions: dim_customer, dim_product, dim_seller, dim_date

Only delivered orders with a delivery date are included. Product categories are translated from Portuguese to English.

Data quality checks

etl/quality_checks.py runs 7 automated checks (rows exist, no null keys, no duplicate order items, no orphan customer/product/seller/date keys). All pass.

Table	Rows loaded
fact_orders	110,189
dim_customer	99,441
dim_product	32,951
dim_seller	3,095
dim_date	714
Key insights
Revenue: R$13.22M in total (item price, excluding freight). January to August revenue grew 141%, from R$2.99M in 2017 to R$7.22M in 2018.
Peak month: November 2017 reached R$988K, up 52% on October, likely driven by Black Friday.
Late deliveries: 6.8% of 96,470 delivered orders arrived after the estimated date.
Impact on reviews: on-time orders average 4.29 stars; late orders average 2.27. This shows association, not proof of cause.
Regional gap: Rio de Janeiro has 12.1% late deliveries on 12,350 orders, versus 4.5% for Sao Paulo on 40,494 orders. Alagoas (21.4%), Maranhao (17.4%) and Sergipe (15.2%) have the highest rates.
Sellers: the top 10 sellers hold 13.3% of revenue; the largest single seller holds 1.7%.
Retention: only 3.0% of customers placed more than one order.
Dashboard

Power BI report with two pages and a page navigator:

Sales overview: total revenue, orders, average review score, late delivery %, monthly revenue trend, top product categories, year filter.
Delivery performance: late delivery rate by state, review score for on-time vs late orders, average delivery days, late orders.

DAX measures: Total Revenue, Total Orders, Late Delivery %, Late Rate, Late Orders, Avg Delivery Days, Avg Review Score.

Sales overview Delivery performance

Project structure
olist-warehouse/
├── data/raw/           (9 CSV files from Kaggle, not committed)
├── data/processed/     (star schema tables as CSV)
├── etl/
│   ├── run_etl.py
│   ├── quality_checks.py
│   └── run_analysis.py
├── sql/analysis.sql    (5 analysis queries)
├── dashboard/          (.pbix file and screenshots)
└── README.md
How to run
Download the dataset from Kaggle: "Brazilian E-Commerce Public Dataset by Olist". Put the 9 CSV files in data/raw/.
Install pandas: pip install pandas
Build the warehouse: python etl/run_etl.py
Check data quality: python etl/quality_checks.py
Run the SQL analysis: python etl/run_analysis.py
Open dashboard/customer_olist.pbix in Power BI Desktop.
SQL techniques used

CTEs, window functions (LAG, RANK), joins across the star schema, conditional aggregation.

Author

S. Jayakumari | B.Tech Artificial Intelligence and
