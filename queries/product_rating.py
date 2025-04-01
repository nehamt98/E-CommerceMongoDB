import argparse
from scripts.db_connect import get_db

# Calculate the average rating and total number of ratings for each product.

def get_product_ratings():
    db = get_db()

    ratings = db.ratings.aggregate([
        {
            "$group": {
                "_id": "$product_id",
                "average_rating": {"$avg": "$rating"},
                "total_ratings": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
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
                "product_id": "$_id",
                "product_name": "$product_details.name",
                "category": "$product_details.category",
                "average_rating": {"$round": ["$average_rating", 1]},
                "total_ratings": 1
            }
        },
        {
            "$sort": {"average_rating": -1}
        }
    ])
    return list(ratings)

def main(args):
    try:
        ratings_list = get_product_ratings()
        if ratings_list:
            print("\nRatings of Products:")
            for idx, product in enumerate(ratings_list, start=1):
                print(f"{idx}. Product: {product['product_name']}")
                print(f"   Category: {product['category']}")
                print(f"   Average Rating: {product['average_rating']:.1f}")
                print(f"   Total Ratings: {product['total_ratings']}")
                print("-" * 30)
        else:
            print("No ratings found.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate average and total ratings for each product.")
    args = parser.parse_args()
    main(args)