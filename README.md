# E-CommerceMongoDB
This project implements a NoSQL document-oriented database in MongoDB for a UK-based online shopping and grocery delivery platform. It was developed to simulate the backend data architecture and functionality for an e-commerce business expanding into fresh grocery delivery via a partner model.

The repository includes MongoDB collection modeling, realistic operational queries, data seeding scripts, and command-line interfaces to simulate backend operations like order placement, partner assignment, inventory tracking, and personalized recommendations.

## Background
The platform merges two business models:
1.	Regular Product Orders – Standard e-commerce orders for books, CDs, phones, and appliances.
2.	Fresh Product Orders – Same-day or instant delivery groceries from local Morrizon stores in Manchester, handled by delivery partners.

The database is designed to support:
- Multiple product categories with complex metadata
- Fresh product logistics using geo-coordinates
- Real-time order processing and driver assignment
- Customer recommendations based on ratings
- Inventory management

## Setup Instructions
### Activate environment
```
conda activate mongo_venv
```
### MongoDB Atlas Setup
- Create a MongoDB Atlas cluster (or run locally)
- Create a database named Amazone
- In scripts/db_connect.py, update your connection string:
```
conn_str = "mongodb+srv://<ID>:<password>@udatabases.a2oqj.mongodb.net/?retryWrites=true&w=majority&appName=UDatabases"
```
- Create collections by loading sample data from the data/ folder or through this script
```
python scripts/seed_database.py
```
## Running the Queries
Each query is implemented as a standalone CLI script inside the queries/ folder.

Each script accepts arguments via --flags.
### insert_fresh_product.py
Function: Add a fresh grocery product to a customer’s cart. If a pending order already exists, update it; else, create a new order.

Usage:
```
python -m queries.insert_fresh_product --customer_id 1 --store_id 1 --product_id 45 --quantity 1
```
### confirm_order.py
Function: Confirm a fresh order and assign the nearest available delivery partner (based on store and driver location).

Usage:
```
python -m queries.confirm_order --customer_id 1 --store_id 1
```
### get_order.py
Function: Fetch detailed info about a shipped fresh order, including products, prices, delivery partner info, and ETA.

Usage:
```
python -m queries.get_order --order_id 2025
```
### list_fresh_products.py
Function: Retrieve fresh grocery products available in nearby stores based on user’s latitude and longitude.

Usage:
```
python -m queries.list_fresh_products --latitude 53.4668 --longitude -2.2339
```
###  sales_by_category.py

Function: Calculate total sales revenue grouped by product category (across fresh and regular products).

Usage:
```
python -m queries.sales_by_category
```
###  inventory_by_warehouse.py
Function: Aggregate and visualize total inventory quantity stored in each warehouse using a pie chart.

Usage:
```
python -m queries.inventory_by_warehouse
```
###  process_delivered_order.py
Function: Move a completed order from current_orders to past_orders, log delivery time, and update driver status.

Usage:
```
python -m queries.process_delivered_order --order_id 2025
```
### customer_recommendations.py
Function: Fetch top recommended products for a customer based on predicted ratings.

Usage:
```
python -m queries.customer_recommendations --customer_id 123
```
### product_rating.py
Function: Calculate the average rating and total number of ratings for each product.

Usage:
```
python -m queries.product_rating
```
### top_customers.py
Function: Display the top 10 customers ranked by total spending.

Usage:
```
python -m queries.top_customers
```