import argparse
import math
from datetime import datetime, timedelta
from scripts.db_connect import get_db

# Update order status when payment is confirmed

def order_confirm(customer_id, store_id):
    
    db = get_db()

    # Step 1: Find the pending order for the customer
    order = db.current_orders.find_one({
        "customer_id": customer_id,
        "category": "fresh",
        "status": "pending",
        "store": store_id
    })
    
    if not order:
        raise ValueError("No pending order found for the customer.")
    
    
    # Step 2: Fetch store details
    store = db.stores.find_one({"store_id": store_id})
    if not store:
        raise ValueError("Store not found")

    store_location = store["location"]

    # Step 3: Find the closest available driver
    drivers = db.amazone_partners.find({
        "on_delivery_errand": False,
        "status": {"$eq": "Active"}
    })

    closest_driver = None
    min_distance = float("inf")

    for driver in drivers:
        driver_location = driver["location"]
        distance = math.sqrt(
            (driver_location["latitude"] - store_location["latitude"])**2 +
            (driver_location["longitude"] - store_location["longitude"])**2
        )
        if distance < min_distance:
            min_distance = distance
            closest_driver = driver

    if not closest_driver:
        raise ValueError("No available drivers")

    # Update driver's status to Active
    db.amazone_partners.update_one(
        {"_id": closest_driver["_id"]},
        {
            "$set": {
                "on_delivery_errand": True
            }
        }
    )
    
    # Step 4: Update the order
    estimated_arrival_time = datetime.now() + timedelta(hours=1)
    db.current_orders.update_one(
        {"_id": order["_id"]},
        {
            "$set": {
                "status": "confirmed",
                "order_date": datetime.now(),
                "driver_id": closest_driver["partner_id"],
                "estimated_arrival_time": estimated_arrival_time
            }
        }
    )
    print(f"Order ID {order['order_id']} confirmed and assigned to driver ID {closest_driver['partner_id']}.")
    return {
        "order_id": order["order_id"],
        "status": "confirmed",
        "driver_id": closest_driver["partner_id"],
        "estimated_arrival_time": estimated_arrival_time
    }

def main(args):
    try:
        result = order_confirm(int(args.customer_id), int(args.store_id))
        print("\nOrder Confirmation Details:")
        print(f"  Order ID: {result['order_id']}")
        print(f"  Status: Confirmed")
        print(f"  Assigned Driver ID: {result['driver_id']}")
        print(f"  Estimated Arrival Time: {result['estimated_arrival_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Confirm a customer's order and assign delivery driver.")

    parser.add_argument("--customer_id", type=int, required=True)
    parser.add_argument("--store_id", type=int, required=True)

    args = parser.parse_args()
    main(args)