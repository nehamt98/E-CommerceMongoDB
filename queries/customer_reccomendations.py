import argparse
from scripts.db_connect import get_db

# Fetch the recommended products for a given customer, sorted by predicted rating.

def get_customer_recommendations(customer_id):
    db = get_db()

    recommendations = db.customers.aggregate([
        {
            "$match": {"customer_id": customer_id}
        },
        {
            "$unwind": "$recommendations"
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "recommendations.product_id",
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
                "product_id": "$recommendations.product_id",
                "predicted_rating": "$recommendations.predicted_rating",
                "product_name": "$product_details.name",
                "category": "$product_details.category"
            }
        },
        {
            "$sort": {"predicted_rating": -1}
        }
    ])

    return list(recommendations)

def main(args):
    try:
        recommendations_list = get_customer_recommendations(int(args.customer_id))
        if recommendations_list:
            print(f"\nTop Recommendations for Customer ID {args.customer_id}:")
            for idx, recommendation in enumerate(recommendations_list, start=1):
                print(f"{idx}. Product: {recommendation['product_name']}")
                print(f"   Category: {recommendation['category']}")
                print(f"   Predicted Rating: {recommendation['predicted_rating']}\n")
        else:
            print("No recommendations found.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get recommended products for a customer.")

    parser.add_argument("--customer_id", type=int, required=True)

    args = parser.parse_args()
    main(args)