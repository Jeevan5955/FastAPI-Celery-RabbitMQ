from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

def dbConnection(app, config):
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    return app.database 

def dbCeleryConnection(celeryapp, config):
    print("Inside dbCeleryConnection")
    celeryapp.mongodb_client = MongoClient(config["ATLAS_URI"])
    celeryapp.database = celeryapp.mongodb_client[config["DB_NAME"]]

def connection():
    print("Triggered Connection")
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]
    return database