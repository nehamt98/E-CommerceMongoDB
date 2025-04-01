import argparse
from datetime import datetime
from scripts.db_connect import get_db

# Question 4
# Query 10 - Move delivered order from current_orders to past_orders

def process_delivered_order(order_id):
    db = get_db()

    # Fetch the order from current_orders
    order = db.current_orders.find_one({"order_id": order_id})
    if not order:
        print("Order not found.")
        return

    # Remove unnecessary fields
    order.pop("estimated_arrival_time", None)  
    order.pop("status", None)                

    # Add the delivery_time field
    order["delivery_time"] = datetime.now()

    # Insert the cleaned order into past_orders
    db.past_orders.insert_one(order)

    # Remove the order from current_orders
    db.current_orders.delete_one({"order_id": order_id})

    # Update the delivery partner's status if it is a fresh order
    if order["category"] == "fresh":
        db.amazone_partners.update_one(
            {"partner_id": order["driver_id"]},
            {"$set": {"on_delivery_errand": False}}
        )

    print(f"Order {order_id} successfully processed with delivery time added.")

def main(args):
    try:
        process_delivered_order(int(args.order_id))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move a delivered order to the past_orders collection.")

    parser.add_argument("--order_id", type=int, required=True)

    args = parser.parse_args()
    main(args)