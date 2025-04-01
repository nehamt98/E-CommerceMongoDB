import os
import json
from pymongo import MongoClient
from scripts.db_connect import get_db

# Path to your data folder
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def seed_data(db):
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            collection_name = filename.replace(".json", "")
            collection = db[collection_name]

            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                    # If it's a list, insert many; else insert one
                    if isinstance(data, list):
                        collection.insert_many(data)
                    else:
                        collection.insert_one(data)
                    print(f"Inserted data into collection: {collection_name}")
                except Exception as e:
                    print(f"Failed to insert {filename}: {e}")

if __name__ == "__main__":
    db = get_db()
    seed_data(db)