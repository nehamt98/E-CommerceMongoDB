import argparse
from scripts.db_connect import get_db

# Retrieve and Display Order Details

def get_order_details(order_id):
    db = get_db()

    # Lookup order details by joining related collections
    order_cursor = db.current_orders.aggregate([
        {
            "$match": {"order_id": order_id}
        },
        {
            "$unwind": "$item"
        },
        {
            "$lookup": {
                "from": "fresh_products",
                "localField": "item.product_id",
                "foreignField": "product_id",
                "as": "product_details"
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "item.product_id",
                "foreignField": "product_id",
                "as": "product_names"
            }
        },
        {
            "$unwind": "$product_details"
        },
        {
            "$unwind": "$product_names"
        },
        {
            "$lookup": {
                "from": "amazone_partners",
                "localField": "driver_id",
                "foreignField": "partner_id",
                "as": "driver_details"
            }
        },
        {
            "$unwind": "$driver_details"
        },
        {
            "$group": {
                "_id": "$order_id",
                "total_cost": {"$first": "$total_cost"},
                "estimated_arrival_time": {"$first": "$estimated_arrival_time"},
                "products": {
                    "$push": {
                        "name": "$product_names.name",
                        "quantity": "$item.quantity",
                        "price": "$product_details.selling_price"
                    }
                },
                "driver": {"$first": "$driver_details.name"}
            }
        }
    ])

    order = next(order_cursor, None)

    if order:
        print(f"Order ID: {order['_id']}")
        print(f"Driver: {order['driver']}")
        print(f"Estimated Arrival: {order['estimated_arrival_time']}")
        print(f"Total Cost: ₹{order['total_cost']}")
        print("Products:")
        for product in order["products"]:
            print(f"  - {product['name']}: {product['quantity']} pcs @ ₹{product['price']}")
    else:
        print(f"No order found with ID {order_id}")

def main(args):
    try:
        get_order_details(int(args.order_id))
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve order details with product and driver info.")

    parser.add_argument("--order_id", type=int, required=True)

    args = parser.parse_args()
    main(args)