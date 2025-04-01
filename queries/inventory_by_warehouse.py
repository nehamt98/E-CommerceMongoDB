import argparse
import pandas as pd
import json
from scripts.db_connect import get_db

# Calculate total inventory levels by warehouse

def inventory_by_warehouse():
    db = get_db()

    inventory_data = db.daily_inventory_level.aggregate([
        {
            "$group": {
                "_id": "$storage_warehouse_name",
                "total_quantity": {"$sum": "$quantity"}
            }
        },
        {
            "$sort": {"total_quantity": -1}  # Sort by highest inventory
        }
    ])

    # Convert results to a Pandas DataFrame
    inventory_list = list(inventory_data)
    inventory_df = pd.DataFrame(inventory_list)
    inventory_df.rename(columns={"_id": "Warehouse", "total_quantity": "Total Quantity"}, inplace=True)

    # Display inventory levels as a table
    print("\nInventory Levels by Warehouse:\n")
    print(inventory_df)

    # Save to JSON file
    with open("Question4_Query9.json", "w") as file:
        json.dump(inventory_list, file, default=str, indent=4)

def main():
    try:
        inventory_by_warehouse()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()