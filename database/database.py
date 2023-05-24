from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

def connection():
    print("Connecting to database")
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]
    return database