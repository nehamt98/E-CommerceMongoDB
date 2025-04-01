import argparse
from datetime import datetime
from scripts.db_connect import get_db

# Insert/Update an order in current_orders when a customer adds a fresh product to cart
def insert_new_fresh_item(customer_id, item, store_id):
    
    db = get_db()

    # Step 1: Fetch product details to calculate total cost
    product = db.fresh_products.find_one({"product_id": item["product_id"]})
    if not product:
        raise ValueError("Product not found")

    total_cost = product["selling_price"] * item["quantity"]
    
    # Step 2: Check if an order already exists for the customer and store
    existing_order = db.current_orders.find_one({
        "customer_id": customer_id,
        "category": "fresh",
        "store": store_id,
        "status": "pending"
    })

    if existing_order:

        existing_item = next(
            (existing for existing in existing_order["item"] if existing["product_id"] == item["product_id"]),
            None
        )

        if existing_item:
            # Update the quantity of the existing item
            db.current_orders.update_one(
                {"_id": existing_order["_id"], "item.product_id": item["product_id"]},
                {"$inc": {"item.$.quantity": item["quantity"]}}
            )
            print(f"Updated quantity of Product ID {item['product_id']} in Order ID: {existing_order['order_id']}")
        else:
            # Get max item no
            max_item_no = max([existing["item_no"] for existing in existing_order["item"]], default=0)
            item["item_no"] = max_item_no + 1
            # Add the new item to the order
            db.current_orders.update_one(
                {"_id": existing_order["_id"]},
                {"$push": {"item": item}}
            )
            print(f"Added new Product ID {item['product_id']} to Order ID: {existing_order['order_id']}")
            
        # Update the total cost
        db.current_orders.update_one(
            {"_id": existing_order["_id"], "item.product_id": item["product_id"]},
            {"$inc": {"total_cost": total_cost}}
        )
        return existing_order
        
    else:
        # Step 3: Create a new order
        last_order = list(db.current_orders.find().sort("order_id", -1).limit(1))
        next_order_id = last_order[0]["order_id"] + 1 if last_order else 1
        item["item_no"] = 1

        # Step 4: Prepare new order data
        new_order = {
            "order_id": next_order_id,
            "total_cost": total_cost,
            "order_date": datetime.now(),
            "customer_id": customer_id,
            "category": "fresh",
            "item": [item],
            "status": "pending",
            "store": store_id
        }

        # Step 5: Insert the new order
        result = db.current_orders.insert_one(new_order)
        print(f"New order created with ID: {new_order['order_id']}")
        return new_order

def main(args):
    item = {
        "product_id": int(args.product_id),
        "quantity": int(args.quantity)
    }
    try:
        insert_new_fresh_item(int(args.customer_id), item, int(args.store_id))
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert fresh item into customer's current order.")

    parser.add_argument("--customer_id", type=int, required=True)
    parser.add_argument("--store_id", type=int, required=True)
    parser.add_argument("--product_id", type=int, required=True)
    parser.add_argument("--quantity", type=int, required=True)

    args = parser.parse_args()
    main(args)