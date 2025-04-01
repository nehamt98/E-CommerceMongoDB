# Import commands
import pymongo
from pymongo import MongoClient

def get_db():
    # Connect to the cluster
    conn_str = "mongodb+srv://nehathomasofficial:nehathomasofficial@udatabases.a2oqj.mongodb.net/?retryWrites=true&w=majority&appName=UDatabases"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        return client.Amazone1
    except Exception:
        print("Unable to connect to the server.")
