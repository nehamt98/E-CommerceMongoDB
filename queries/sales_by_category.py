import argparse
from scripts.db_connect import get_db

# Calculate total sales revenue per category

def calculate_sales_by_category():
    db = get_db()

    sales_data = db.past_orders.aggregate([
        {
            "$unwind": "$item"
        },
        # Join with the products collection to get the category
        {
            "$lookup": {
                "from": "products",
                "localField": "item.product_id",
                "foreignField": "product_id",
                "as": "product_details"
            }
        },
        {
            "$unwind": "$product_details"
        },
        # Dynamically join with fresh_products
        {
            "$lookup": {
                "from": "fresh_products",
                "let": {"product_id": "$item.product_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$product_id", "$$product_id"]}}}
                ],
                "as": "fresh_product_details"
            }
        },
        # Dynamically join with regular_products
        {
            "$lookup": {
                "from": "regular_products",
                "let": {"product_id": "$item.product_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$product_id", "$$product_id"]}}}
                ],
                "as": "regular_product_details"
            }
        },
        # Compute the actual selling price
        {
            "$addFields": {
                "category": "$product_details.category",
                "selling_price": {
                    "$cond": {
                        "if": {"$gt": [{"$size": "$fresh_product_details"}, 0]},
                        "then": {"$arrayElemAt": ["$fresh_product_details.selling_price", 0]},
                        "else": {"$arrayElemAt": ["$regular_product_details.selling_price", 0]}
                    }
                }
            }
        },
        # Calculate revenue
        {
            "$group": {
                "_id": "$category",
                "total_revenue": {
                    "$sum": {
                        "$multiply": ["$item.quantity", "$selling_price"]
                    }
                }
            }
        }
    ])

    print("Total Sales Revenue per Category:\n")
    for row in sales_data:
        print(f"  - {row['_id']}: ₹{round(row['total_revenue'], 2)}")

def main(args):
    try:
        calculate_sales_by_category()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate total sales revenue per category.")
    args = parser.parse_args()
    main(args)