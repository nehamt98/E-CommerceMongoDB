# Import commands
import pymongo
from pymongo import MongoClient

def get_db():
    # Replace ID and password to connect to your cluster
    conn_str = "mongodb+srv://<ID>:<password>@udatabases.a2oqj.mongodb.net/?retryWrites=true&w=majority&appName=UDatabases"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        return client.Amazone1
    except Exception:
        print("Unable to connect to the server.")
