from scripts.db_connect import get_db

# Identify top 10 customers by total spending.

def get_top_customers():
    db = get_db()

    top_customers = db.past_orders.aggregate([
        {
            "$group": {
                "_id": "$customer_id",
                "total_spent": {"$sum": "$total_order_cost"}
            }
        },
        {
            "$sort": {"total_spent": -1}
        },
        {
            "$limit": 10
        },
        {
            "$lookup": {
                "from": "customers",
                "localField": "_id",
                "foreignField": "customer_id",
                "as": "customer_details"
            }
        },
        {
            "$unwind": "$customer_details"
        },
        {
            "$project": {
                "_id": 0,
                "customer_id": "$_id",
                "name": "$customer_details.name",
                "total_spent": {"$round": ["$total_spent", 2]}
            }
        }
    ])
    return list(top_customers)

def main():
    try:
        customers_list = get_top_customers()
        if customers_list:
            print("\nTop 10 Customers by Spending:")
            for idx, customer in enumerate(customers_list, start=1):
                print(f"{idx}. Name: {customer['name']}")
                print(f"   Customer ID: {customer['customer_id']}")
                print(f"   Total Spent: £{customer['total_spent']:.2f}")
                print("-" * 30)

        else:
            print("No customers found.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()