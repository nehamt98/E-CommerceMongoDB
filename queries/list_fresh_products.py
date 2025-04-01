import argparse
import math
from scripts.db_connect import get_db

# Get list of fresh products according to user's location

def get_fresh_products(user_location):
    db = get_db()
    nearby_stores = []
    user_lat, user_lon = user_location

    # Fetch all stores with fresh products
    stores = db["stores"].find()
    for store in stores:
        store_lat = store['location']['latitude']
        store_lon = store['location']['longitude']
        distance = math.sqrt(
            (user_lat - store_lat)**2 +
            (user_lon - store_lon)**2
        )

        # Assuming a threshold for distance (e.g., 0.1 degrees ~ 10 km)
        if distance <= 0.1:
            nearby_stores.append(store['store_id'])

    # Aggregate results
    fresh_products = db.fresh_products.aggregate([
        {
            "$match": {
                "store_id": {"$in": nearby_stores}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "product_id",
                "foreignField": "product_id",
                "as": "product_details"
            }
        },
        {
            "$unwind": "$product_details"
        },
        {
            "$project": {
                "_id": 0,
                "name": "$product_details.name",
                "category": 1,
                "description": 1,
                "price": "$selling_price",
            }
        }
    ])

    print("Fresh Products near you:\n")
    for product in fresh_products:
        print(f"  - {product['name']} ({product['category']}): ₹{product['price']}")
        print(f"    Description: {product.get('description', 'N/A')}\n")

def main(args):
    try:
        latitude = float(args.latitude)
        longitude = float(args.longitude)
        get_fresh_products((latitude, longitude))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List nearby fresh products based on location.")

    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)

    args = parser.parse_args()
    main(args)