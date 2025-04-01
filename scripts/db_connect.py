# Import commands
import pymongo
from pymongo import MongoClient

def get_db():
    # Connect to the cluster
    conn_str = "mongodb+srv://<ID>:<password>@udatabases.a2oqj.mongodb.net/?retryWrites=true&w=majority&appName=UDatabases"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        print(client.server_info())
    except Exception:
        print("Unable to connect to the server.")
    return client.Amazone
