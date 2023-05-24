from celery import shared_task
from api import callApi
from bson import ObjectId
from database.database import connection
import json
from datetime import datetime, timedelta
import requests
import requests

database = connection()

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='user:Create User Post.')
def savingUser(self,data):
    try:
        database["userinfo"].insert_one(data)
    except Exception as e:
        print("Exception here :",e)
        pass

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='user:Update User Post.')
def updateUser(self,data):
    
    filter = { "_id": ObjectId(data["id"]) }
    del data["id"]
    newvalues = { "$set": data }
    print("filter :",filter)
    print("newvalues :",newvalues)
    try:
        database["userinfo"].update_one(filter,newvalues)
    except Exception as e:
        print("Exception here :",e)
        pass

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='user:Delete User Post.')
def deleteUser(self,data):
    
    filter = { "_id": ObjectId(data["id"]) }
    try:
        database["userinfo"].delete_one(filter)
    except Exception as e:
        print("Exception here :",e)
        pass

